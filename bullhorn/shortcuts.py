from bullhorn.models import Category, Metadata, Tag, Contact, Node, Event
from django import forms
from datetime import datetime
from django.shortcuts import get_object_or_404
import re


def get_page_type_from_url(path):
    page_types = {'device': Node, 'event': Event, 'contact': Contact,
                  'tag': Tag, 'tagtype': Category}
    page_type = re.match('/(\w+)/?', path).group(1)
    return (page_type, page_types[page_type])


def metadata_as_json():
    return Metadata.objects.values_list('display_name', flat=True)


def contacts_to_string(contacts):
    result = [x.email for x in contacts]
    return ','.join(result)


def contact_from_user(user):
    contact = Contact()
    contact.first_name = user.first_name
    contact.last_name = user.last_name
    contact.email = user.email
    contact.save()
    return contact


def tags_to_dict(tags):
    tags_dict = {}
    for tag in tags:
        category = tags_dict.get(tag.category.name, [])
        category.append(tag.metadata.name)
        tags_dict[tag.category.name] = category
    tags_dict = {key: "%s" % ','.join(value)
                 for (key, value) in tags_dict.iteritems()}
    return tags_dict


def categories_for_forms(include_device=False):
    if include_device:
        return Category.objects.all()
    else:
        return Category.objects.exclude(name='device')


def update_model_from_form(model, form):
    category_names = get_tag_fields()
    contacts = []
    many_to_many = {}
    for field in form.fields:
        value = form.cleaned_data[field]
        if field == 'event_date':  # Need to make check more generic
            value = form.cleaned_data[field].isoformat()

        if field == 'contacts':
            contacts = get_metadata(value)
            contacts = process_contacts(contacts)

        if not field in category_names:
            setattr(model, field, value)
    tags = process_tags_in_form(form)
    model.save()
    many_to_many['tags'] = tags
    many_to_many['contacts'] = contacts
    for tag in ('tags', 'contacts'):
        if hasattr(model, tag):
            setattr(model, tag, many_to_many[tag])
    return model


def process_contacts(contacts):
    contact_objects = []
    for contact in contacts:
        record = Contact.objects.get_or_create(email=normalize_string(contact))
        contact_objects.append(record[0])
    return contact_objects


def process_form(request, form_type, *args):
    categories = Category.objects.all()
    if request.POST:
        form = form_type(request.POST)
        if form.is_valid():
            form.save(*args)
            empty_form = form_type()
            template_variables = {'form': empty_form,
                                  'categories': categories,
                                  'success_message':
                                  'Record successfully created',
                                  'metadata': metadata_as_json()}
        else:
            template_variables = {'form': form,
                                  'categories': categories,
                                  'metadata': metadata_as_json()}
    else:
        form = form_type()
        template_variables = {'form': form, 'categories': categories,
                              'metadata': metadata_as_json()}
    return template_variables


def process_tags_in_form(form, include_device=False):
    categories = categories_for_forms(include_device)
    tags = []
    for category in categories:
        values = form.cleaned_data[normalize_string(category.name)]
        if values:  # Ensure this field has data or we create emptyt tags
            metadata_values = get_metadata(values)
            for metadata in metadata_values:
                metadata_object = Metadata.objects.get_or_create(
                    name=normalize_string(metadata))
                if metadata_object[1]:
                    metadata_object[0].display_name = metadata
                    metadata_object[0].save()
                tag = Tag.objects.get_or_create(metadata=metadata_object[0],
                                                category=category)
                tags.append(tag[0])
    return tags


def categories_as_form_fields(include_device=False):
    fields = {}
    categories = categories_for_forms(include_device)
    for category in categories:
        name = normalize_string(category.name)
        fields[name] = forms.CharField(max_length=500,
                                       label=category.name,
                                       required=False,
                                       widget=forms.TextInput(attrs={
                                           'class': 'tags input-xxlarge'}
                                       ))
    return fields


def normalize_string(text):
    return text.strip().replace(" ", "_").lower()


def get_metadata(text):
    return text.split(",")


def get_tag_fields():
    categories = categories_for_forms(include_device=True)
    fields = [normalize_string(category.name)
              for category in categories]
    fields.append('contacts')
    return fields


def convert_to_date(dt):
    return datetime.strptime(dt, "%Y-%m-%d %H:%M:%S").date()


def get_query_string(request):
    results = {}
    try:
        query_string = request.META['QUERY_STRING']
        if query_string:
            parameters = query_string.split("&")
            for parameter in parameters:
                key, value = parameter.split("=")
                results[key] = value
    except KeyError:
        pass
    return results


def get_model_fields(model):
    if not isinstance(model, type(model)):
            model = type(model)()
    fields = [x.name for x in model._meta.fields]
    many_to_many = [x.name for x in model._meta.many_to_many]
    return fields, many_to_many


def save_form_to_db(form, model):

    success = False
    if form.is_valid():
        update_model_from_form(model, form)
        success_message = "Record successfully updated"
        success = True
        empty_form = type(form)()
        template_variables = {'form': empty_form,
                              'success_message': success_message,
                              'model': model}
    else:
        template_variables = {'form': form, 'model': model,
                              'update': True}
    return (template_variables, success)


def populate_form_from_model(form_type, model_object):

    form_fields = {}
    fields, many_to_many = get_model_fields(model_object)
    for field in fields:
        if not field == 'id':
            form_fields[field] = getattr(model_object, field)
    for field in many_to_many:
        if field == 'contacts':
            contacts = model_object.contacts.all()
            form_fields[field] = contacts_to_string(contacts)
        else:
            tags = model_object.tags.all()
            tags_dict = tags_to_dict(tags)
            tags_dict = {normalize_string(key): value
                         for (key, value) in tags_dict.iteritems()}
            form_fields.update(tags_dict)
            form = form_type(initial=form_fields)
            template_variables = {'form': form, 'update': True}
    return template_variables


def edit_form(request, model, form_type, pk_id):
    model_object = get_object_or_404(model, pk=pk_id)
    if request.POST:
        form = form_type(request.POST)
        results = save_form_to_db(form, model_object)
        template_variables = results[0]
    else:
        template_variables = populate_form_from_model(form_type, model_object)
    return template_variables
