from django import forms
from django.forms import ModelForm, Textarea
from bullhorn.models import Category, Event, Metadata, Contact, Tag, Node
from bullhorn.utils import normalize_string, get_metadata


class NodeForm(forms.Form):

    name = forms.CharField(max_length=200)
    description = forms.CharField(required=False,
                                  widget=forms.Textarea(
                                      attrs={'class': 'input-xxlarge'}))

    def __init__(self, *args, **kwargs):
        super(NodeForm, self).__init__(*args, **kwargs)
        categories = Category.objects.all()
        for category in categories:
            name = normalize_string(category.name)
            self.fields[name] = forms.CharField(max_length=500,
                                                label=category.name,
                                                required=False,
                                                widget=forms.TextInput(attrs={
                                                    'class': 'input-xxlarge'}
                                                ))

    def save(self):
        categories = Category.objects.all()
        tags = []
        for category in categories:
            values = self.cleaned_data[normalize_string(category.name)]
            metadata_values = get_metadata(values)
            for metadata in metadata_values:
                metadata_object = Metadata.objects.get_or_create(
                    name=normalize_string(metadata))
                tag = Tag.objects.get_or_create(metadata=metadata_object[0],
                                                category=category)
                tags.append(tag[0])
        node = Node()
        node.name = self.cleaned_data['name']
        node.description = self.cleaned_data['description']
        node.save()
        node.tags.add(*tags)


class CategoryForm(ModelForm):

    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'description': Textarea()
        }

    def is_unique(self):
        value = self.cleaned_data['name'].replace(" ", "_").lower()
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
    tags = forms.CharField(max_length=500,
                           widget=forms.TextInput(
                               attrs={'class': 'input-xxlarge'}))
    contacts = forms.CharField(max_length=500,
                               widget=forms.TextInput(
                                   attrs={'class': 'input-xxlarge'}))
    event_date = forms.DateTimeField()

    def save(self):
        tags = self.cleaned_data['tags'].split(",")
        contacts = self.cleaned_data['contacts'].split(",")
        tag_db_objects = []
        contact_db_objects = []
        for tag in tags:
            tag = normalize_string(tag)
            result = Metadata.objects.get_or_create(name=tag)
            tag_db_objects.append(result[0])
        for contact in contacts:
            result = Contact.objects.get_or_create(email=contact)
            contact_db_objects.append(result[0])
        new_event = Event()
        for field in ('name', 'short_description', 'description',
                      'event_date'):
            setattr(new_event, field, self.cleaned_data[field])
        new_event.save()
        new_event.tags.add(*tag_db_objects)
        new_event.contacts.add(*contact_db_objects)


class ContactForm(ModelForm):
    class Meta:
        model = Contact


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs={'class': 'input-block-level',
               'placeholder': 'Email Address'}))

    password = forms.CharField(max_length=50,
                               widget=forms.PasswordInput(attrs={
                               'class': 'input-block-level',
                               'placeholder': 'Password'}))
