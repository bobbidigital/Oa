from django import forms
from django.forms import ModelForm, Textarea
from bullhorn.models import Category, Event, Metadata, Contact
from bullhorn.utils import normalize


class NodeForm(forms.Form):

    name = forms.CharField(max_length=100)
    description = forms.CharField(max_length=500, required=False)

    def __init__(self, *args, **kwargs):
        super(NodeForm, self).__init__(*args, **kwargs)
        categories = Category.objects.all()
        for category in categories:
            name = self.normalize_string(category.name)
            self.fields[name] = forms.CharField(max_length=500,
                                                label=category.name,
                                                required=False)

    def normalize_string(self, text):
        return text.replace(" ", "_").lower()


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

    name = forms.CharField(max_length=200)
    short_description = forms.CharField(max_length=50)
    description = forms.CharField(max_length=500,
                                  widget=Textarea(
                                      attrs={'cols': '100'}))
    tags = forms.CharField(max_length=500)
    contacts = forms.CharField(max_length=500)
    event_date = forms.DateTimeField()

    def save(self):
        tags = self.cleaned_data['tags'].split(",")
        contacts = self.cleaned_data['contacts'].split(",")
        tag_db_objects = []
        contact_db_objects = []
        for tag in tags:
            tag = normalize(tag)
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
