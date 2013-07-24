from django import forms
from django.forms import ModelForm, Textarea
from bullhorn.models import Tag, Category, Event
from bullhorn.models import Metadata, Contact, Node, Alert
from bullhorn.shortcuts import process_tags_in_form, categories_for_forms
from bullhorn.shortcuts import categories_as_form_fields
from bullhorn.shortcuts import normalize_string, get_metadata
from django.core.exceptions import ObjectDoesNotExist


class NodeForm(forms.Form):

    name = forms.CharField(max_length=200)
    description = forms.CharField(required=False,
                                  widget=forms.Textarea(
                                      attrs={'class': 'input-xxlarge'}))

    def __init__(self, *args, **kwargs):
        super(NodeForm, self).__init__(*args, **kwargs)
        categories = categories_for_forms()
        for category in categories:
            name = normalize_string(category.name)
            self.fields[name] = forms.CharField(max_length=500,
                                                label=category.name,
                                                required=False,
                                                widget=forms.TextInput(attrs={
                                                    'class': 'tags input-xxlarge'}
                                                ))

    def save(self):
        tags = process_tags_in_form(self)
        node = Node()
        node.name = self.cleaned_data['name']
        metadata = Metadata.objects.get_or_create(name=node.name)
        category = Category.objects.get(pk=1)
        device_tag = Tag.objects.get_or_create(category=category,
                                               metadata=metadata[0])

        node.description = self.cleaned_data['description']
        node.save()
        node.tags.add(*tags)
        node.tags.add(device_tag[0])


class CategoryForm(ModelForm):

    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'description': Textarea()
        }

    def is_unique(self):
        value = normalize_string(self.cleaned_data['name'])
        return Category.objects.filter(name=value).count() == 0


class EventForm(forms.Form):

    name = forms.CharField(max_length=200,
                           widget=forms.TextInput(
                           attrs={'class': 'input-xxlarge'}))

    short_description = forms.CharField(max_length=500,
                                        widget=forms.TextInput(
                                        attrs={'class': 'input-xxlarge'}))
    description = forms.CharField(widget=Textarea(
                                  attrs={'class': 'input-xxlarge'}))
    contacts = forms.CharField(max_length=500,
                               widget=forms.TextInput(
                                   attrs={'class': 'input-xxlarge'}))
    event_date = forms.DateTimeField()

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        fields = categories_as_form_fields(include_device=True)
        self.fields.update(fields)

    def save(self):
        tags = process_tags_in_form(self)
        contacts = get_metadata(self.cleaned_data['contacts'])
        contact_db_objects = []
        for contact in contacts:
            result = Contact.objects.get_or_create(email=contact)
            contact_db_objects.append(result[0])
        new_event = Event()
        for field in ('name', 'short_description', 'description',
                      'event_date'):
            setattr(new_event, field, self.cleaned_data[field])
        new_event.save()
        new_event.tags = tags
        new_event.contacts.add(*contact_db_objects)


class ContactForm(ModelForm):
    class Meta:
        model = Contact
        exclude = ['user']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs={'class': 'input-block-level',
               'placeholder': 'Email Address'}))

    password = forms.CharField(max_length=50,
                               widget=forms.PasswordInput(attrs={
                               'class': 'input-block-level',
                               'placeholder': 'Password'}))


class AlertForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(AlertForm, self).__init__(*args, **kwargs)
        categories = categories_for_forms()
        for category in categories:
            name = normalize_string(category.name)
            self.fields[name] = forms.CharField(max_length=500,
                                                label=category.name,
                                                required=False,
                                                widget=forms.TextInput(attrs={
                                                    'class': 'tags input-xxlarge'}
                                                ))

    def save(self, user):
        tags = process_tags_in_form(self)
        contact = Contact.objects.get(email=user.email)
        try:
            alert = Alert.objects.get(contact=contact)
        except ObjectDoesNotExist:
            alert = Alert()
            alert.contact = contact
            alert.save()
        alert.tags = tags


class UserForm(forms.Form):

    first_name = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs={'class': 'input-block-level',
               'placeholder': 'First Name'}))

    last_name = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs={'class': 'input-block-level',
               'placeholder': 'Last Name'}))

    email = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs={'class': 'input-block-level',
               'placeholder': 'Email Address'}))

    password = forms.CharField(max_length=50, widget=forms.PasswordInput(
        attrs={'class': 'input-block-level',
               'placeholder': 'Password'}))

    confirm_password = forms.CharField(max_length=50,
                                       widget=forms.PasswordInput(
                                       attrs={'class': 'input-block-level',
                                              'placeholder': 'Confirm Password'}))

    def is_valid(self):
        valid = super(UserForm, self).is_valid()
        if valid:
            valid = self.cleaned_data['password'] == (
                self.cleaned_data['confirm_password'])
            if not valid:
                self.errors['password'] = ['Passwords do not match']
        return valid
