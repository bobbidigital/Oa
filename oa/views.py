# Create your views here.
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from bullhorn.forms import CategoryForm, EventForm, ContactForm, UserForm
from bullhorn.forms import NodeForm, LoginForm, AlertForm
from bullhorn.models import Category, Event, Contact, Node
from bullhorn.models import Tag, Alert, Metadata
from bullhorn.shortcuts import process_form, categories_for_forms
from bullhorn.shortcuts import normalize_string, update_model_from_form
from bullhorn.shortcuts import contacts_to_string, tags_to_dict
from bullhorn.shortcuts import contact_from_user, get_query_string
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import datetime


def index(request):
    categories = Category.objects.all()
    events = Event.objects.select_related().filter(
        event_date__gte=datetime.date.today()).order_by('event_date')
    return render_to_response('index.html', {'categories': categories,
                                             'events': events},
                              context_instance=RequestContext(request))


def node(request):
    categories = Category.objects.all()
    nodes = Node.objects.all().order_by('name')
    return render_to_response('node.html', {'categories': categories,
                                            'nodes': nodes},
                              context_instance=RequestContext(request))


def add_tagtype(request):
    categories = Category.objects.all()
    if request.POST:
        form = CategoryForm(request.POST)
        if form.is_valid() and form.is_unique():
            form.save()
            empty_form = CategoryForm()
            template_variables = {'form': empty_form,
                                  'success_message': "%s created successfully"
                                  % form.cleaned_data['name'],
                                  'categories': categories}
        else:
            template_variables = {'form': form, 'categories': categories}

    else:
        form = CategoryForm()
        template_variables = {'form': form, 'categories': categories}
    return render_to_response('new_category.html', template_variables,
                              context_instance=RequestContext(request))


def event(request):
    categories = Category.objects.all()
    events = Event.objects.select_related().filter(
        event_date__gte=datetime.date.today()).order_by('event_date')
    return render_to_response('event.html', {'categories': categories,
                                             'events': events},
                              context_instance=RequestContext(request))


def view_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    categories = categories_for_forms(include_device=True)
    template_variables = {'event': event, 'categories': categories}
    return render_to_response('view_event.html', template_variables,
                              context_instance=RequestContext(request))


def edit_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    redirect = False
    if request.POST:
        form = EventForm(request.POST)
        if form.is_valid():
            update_model_from_form(event, form)
            empty_form = EventForm()
            success_message = "Record successfully updated"
            template_variables = {'form': empty_form,
                                  'success_message': success_message,
                                  'event': event}
            template = 'view_event.html'
            redirect = True
        else:
            template_variables = {'form': form, 'event': event,
                                  'update': True}
            template = 'new_event.html'
    else:
        fields = {'name': event.name,
                  'short_description': event.short_description,
                  'description': event.description,
                  'event_date': event.event_date}
        contacts = event.contacts.all()
        contact_string = contacts_to_string(contacts)
        tags = event.tags.all()
        tags_dict = tags_to_dict(tags)
        tags_dict = {normalize_string(key): value
                     for (key, value) in tags_dict.iteritems()}
        fields.update(tags_dict)
        fields.update({'contacts': contact_string})
        form = EventForm(initial=fields)
        template_variables = {'form': form, 'url': '/event/edit/%s' % event_id,
                              'update': True}
        template = 'new_event.html'
    if redirect:
        return HttpResponseRedirect("/event/view/%s" % event.id)
    else:
        return render_to_response(template, template_variables,
                                  context_instance=RequestContext(request))


def add_event(request):
    template_variables = process_form(request, EventForm)
    metadata = Metadata.objects.values_list('name', flat=True)
    template_variables['url'] = '/event/add'
    template_variables['metadata'] = metadata
    return render_to_response('new_event.html', template_variables,
                              context_instance=RequestContext(request))


def contact(request):
    categories = Category.objects.all()
    contacts = Contact.objects.all()
    template_variables = {'categories': categories, 'contacts': contacts}
    return render_to_response('contact.html', template_variables,
                              context_instance=RequestContext(request))


def add_contact(request):
    template_variables = process_form(request, ContactForm)
    return render_to_response('new_contact.html', template_variables,
                              context_instance=RequestContext(request))


def add_node(request):
    template_variables = process_form(request, NodeForm)
    return render_to_response('new_device.html', template_variables,
                              context_instance=RequestContext(request))


def view_node(request, node_id):
    node = get_object_or_404(Node, pk=node_id)
    categories = Category.objects.all()
    template_variables = {'categories': categories, 'node': node}
    return render_to_response('view_node.html', template_variables,
                              context_instance=RequestContext(request))


def tagtype(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    categories = Category.objects.all()
    nodes = Node.objects.filter(tags__category=category)
    tags = Tag.objects.filter(category=category)

    ##ToDo:
    ##Ugly hack. Real problem is Event class isn't handling metadat/tags
    ##correctly
    metadata = [tag.metadata.name for tag in tags]
    events = Event.objects.filter(tags__metadata__name__in=metadata
                                  ).distinct().order_by('event_date')
    template_variables = {'categories': categories, 'nodes': nodes,
                          'node_count': nodes.count() or 0, 'tags': tags,
                          'tag_count': tags.count() or 0, 'category': category,
                          'event_count': events.count() or 0, 'events': events}
    return render_to_response('category.html', template_variables,
                              context_instance=RequestContext(request))


def login_view(request):

    query_strings = get_query_string(request)
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])
            template_variables = {}
            template = ''
            if not user:
                template_variables = {'error': 'Username/Password failed',
                                      'form': LoginForm()}
                template = 'login.html'
                return render_to_response(template,
                                          template_variables,
                                          context_instance=RequestContext(
                                              request))

            if not user.is_active:
                template_variables = {'error': 'User account is not active',
                                      'form': LoginForm()}
                template = 'login.html'
            else:
                login(request, user)
                request.session.set_expiry(900)
                ##Todo Refactor out the view logic and have both views call
                #the same function. Possibly rendering twice here.
                try:
                    url = query_strings['next']
                except KeyError:
                    url = "/"
                return HttpResponseRedirect(url)
        else:
            template = 'login.html'
            template_variables = {'error': 'All fields are required',
                                  'form': form}
    else:
        template_variables = {'form': LoginForm()}
        template = 'login.html'

    return render_to_response(template, template_variables,
                              context_instance=RequestContext(request))


def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")


@login_required(login_url='/login')
def add_alert(request):
    template_variables = process_form(request, AlertForm, request.user)
    return render_to_response('new_alert.html', template_variables,
                              context_instance=RequestContext(request))


@login_required(login_url='/login')
def alert(request, contact_id=None):
    if not contact_id:
        contact = get_object_or_404(Contact, user=request.user)
    else:
        contact = get_object_or_404(Contact, pk=contact_id)

    alerts = Alert.objects.filter(contact=contact)
    categories = Category.objects.all()
    template_variables = {'contact': contact, 'alerts': alerts[0],
                          'categories': categories}
    return render_to_response('alert.html', template_variables,
                              context_instance=RequestContext(request))


def view_tag(request, tag_id):
    tag = get_object_or_404(Tag, pk=tag_id)
    template_variables = {}
    template_variables['tag'] = tag
    events = Event.objects.filter(tags=tag,
                                  event_date__gte=datetime.datetime.today()
                                  ).order_by('event_date')
    devices = Node.objects.filter(tags=tag)
    template_variables['events'] = events
    template_variables['devices'] = devices
    return render_to_response('view_tags.html', template_variables,
                              context_instance=RequestContext(request))


def create_account(request):
    if request.POST:
        form = UserForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(form.cleaned_data['email'],
                                            form.cleaned_data['email'],
                                            form.cleaned_data['password'])
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            contact = contact_from_user(user)
            template_variables = {'form': UserForm(), 'success': True,
                                  'contact': contact}
        else:
            template_variables = {'form': form}
    else:
        template_variables = {'form': UserForm()}
    return render_to_response('accountcreate.html', template_variables,
                              context_instance=RequestContext(request))
