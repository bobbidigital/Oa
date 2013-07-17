from django.test import TestCase
from bullhorn.forms import NodeForm, EventForm
from bullhorn.models import Category, Contact, Event, Metadata


class NodeFormTest(TestCase):

    categories = ['Applications', 'Business Units', 'Locations']

    def setUp(self):
        for category in self.categories:
            Category(name=category).save()

    def test_form_instantiation(self):
        value_string = "Valid Text"
        data = {}
        for category in self.categories:
            category = category.replace(" ", "_").lower()
            data[category] = value_string
        data['name'] = 'Jeff'
        form = NodeForm(data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['business_units'], value_string)


class EventFormTest(TestCase):

    tags = ['eStore', 'ICAdmin']
    form_values = {'name': 'PTC Maintenance',
                   'short_description': 'Maintenance window for switch',
                   'description': 'Just more maintenance detail',
                   'tags': 'eStore,ICAdmin',
                   'contacts': 'jeffery.smith@wolterskluwer.com',
                   'event_date': '2013-10-11 14:25:00'
                   }

    def setUp(self):
        contact = Contact()
        contact.first_name = "Jeffery"
        contact.last_name = "Smith"
        contact.email = "jeffery.smith@wolterskluwer.com"
        contact.save()

    def test_form_save(self):
        form = EventForm(self.form_values)
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(Event.objects.all().count(), 1)
        self.assertEqual(Metadata.objects.filter(name='icadmin').count(), 1)
        self.assertEqual(Metadata.objects.filter(name='estore').count(), 1)
