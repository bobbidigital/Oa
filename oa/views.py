# Create your views here.
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from bullhorn.forms import UserForm
from bullhorn.forms import LoginForm, AlertForm
from bullhorn.models import Category, Event, Contact, Node
from bullhorn.models import Tag, Alert
from bullhorn.shortcuts import process_form, categories_for_forms
from bullhorn.shortcuts import contact_from_user, get_query_string, edit_form
from bullhorn.shortcuts import get_page_type_from_url
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


def model(request):
    page_type, model = get_page_type_from_url(request.path)
    categories = Category.objects.all()
    if model.__name__ == 'Event':
        model_instances = model.objects.filter(
            event_date__gte=datetime.date.today()).order_by('event_date')
    else:
        model_instances = model.objects.all()
    template = '%s.html' % page_type
    return render_to_response(template, {'categories': categories,
                                         'models': model_instances},
                              context_instance=RequestContext(request))


def edit_model(request, model_id):
    page_type, model = get_page_type_from_url(request.path)
    form = globals()['%sForm' % model.__name__]
    template = 'new_%s.html' % page_type
    template_variables = edit_form(request, model, form, model_id)
    if 'success_message' in template_variables:
        return HttpResponseRedirect("/%s/view/%s" % (page_type, model_id))
    else:
        template_variables['url'] = '/%s/edit/%s' % (page_type, model_id)
        return render_to_response(template, template_variables,
                                  context_instance=RequestContext(request))


def view_model(request, model_id):
    page_type = get_page_type_from_url(request.path)
    categories = categories_for_forms(include_device=True)
    model = page_type[1]
    model_instance = get_object_or_404(model, pk=model_id)
    template_variables = {'model': model_instance, 'categories': categories}
    template = 'view_%s.html' % page_type[0]
    return render_to_response(template, template_variables,
                              context_instance=RequestContext(request))


def add_model(request):
    page_type, model = get_page_type_from_url(request.path)
    form_type = globals()['%sForm' % model.__name__]
    template_variables = process_form(request, form_type)
    template_variables['url'] = '/%s/add' % page_type
    template = 'new_%s.html' % page_type
    return render_to_response(template, template_variables,
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
