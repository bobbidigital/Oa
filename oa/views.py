# Create your views here.
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from bullhorn.forms import CategoryForm, EventForm, ContactForm, NodeForm
from bullhorn.models import Category, Event, Contact, Node, Tag
from bullhorn.shortcuts import process_form
import datetime


def index(request):
    categories = Category.objects.all()
    events = Event.objects.select_related().filter(
        event_date__gte=datetime.date.today()).order_by('event_date')
    return render_to_response('index.html', {'categories': categories,
                                             'events': events},
                              context_instance=RequestContext(request))


def add_node(request):
    pass


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
        event_date__gte=datetime.date.today())
    return render_to_response('event.html', {'categories': categories,
                                             'events': events},
                              context_instance=RequestContext(request))


def view_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    return render_to_response('view_event.html', {'event': event},
                              context_instance=RequestContext(request))


def add_event(request):
    template_variables = process_form(request, EventForm)
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


def add_device(request):
    template_variables = process_form(request, NodeForm)
    return render_to_response('new_device.html', template_variables,
                              context_instance=RequestContext(request))


def tagtype(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    categories = Category.objects.all()
    nodes = Node.objects.filter(tags__category=category)
    tags = Tag.objects.filter(category=category)
    template_variables = {'categories': categories, 'nodes': nodes,
                          'node_count': nodes.count(), 'tags': tags,
                          'tag_count': tags.count(), 'category': category}
    return render_to_response('category.html', template_variables,
                              context_instance=RequestContext(request))
