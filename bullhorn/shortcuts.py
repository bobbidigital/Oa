from bullhorn.models import Category, Metadata, Tag, Contact
from django import forms
from datetime import datetime


def contacts_to_string(contacts):
    result = [x.email for x in contacts]
    return ','.join(result)


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
    try:
        model.tags = tags
    except AttributeError:
        pass

    try:
        model.contacts = contacts
    except AttributeError:
        pass
    model.save()
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
                                  'Record successfully created'}
        else:
            template_variables = {'form': form,
                                  'categories': categories}
    else:
        form = form_type()
        template_variables = {'form': form, 'categories': categories}
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
                    name=normalize_string(metadata),
                    display_name=metadata)
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
                                           'class': 'input-xxlarge'}
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
