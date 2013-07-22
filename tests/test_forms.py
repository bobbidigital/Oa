from django.test import TestCase
from bullhorn.forms import NodeForm, EventForm, AlertForm
from bullhorn.models import Category, Contact, Event, Tag, Alert
from bullhorn.utils import normalize_string


class DummyObject(object):
    pass


class NodeFormTest(TestCase):

    categories = ['Applications', 'Business Units', 'Locations']
    form_values = {'name': 'WKLEGAFJWEBFP01',
                   'description': 'Node for the AFJ Web Server',
                   'applications': 'web server,AFJ,apache',
                   'business_units': 'TAA',
                   'locations': 'ptc-k,front end'}

    def setUp(self):
        category = Category(name='Device')
        category.save()
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

    def test_tag_save(self):
        form = NodeForm(self.form_values)
        self.assertTrue(form.is_valid())
        form.save()
        tags = Tag.objects.all().exclude(category__id=1)
        for tag in tags:
            expected_values = self.form_values[normalize_string(
                tag.category.name)]
            expected_values = [normalize_string(
                x) for x in expected_values.split(",")]
            self.assertTrue(tag.metadata.name in expected_values)
        tag = Tag.objects.get(category__id=1)
        self.assertTrue(tag)


class EventFormTest(TestCase):

    tags = ['eStore', 'ICAdmin']
    form_values = {'name': 'PTC Maintenance',
                   'short_description': 'Maintenance window for switch',
                   'description': 'Just more maintenance detail',
                   'applications': 'eStore,ICAdmin',
                   'contacts': 'jeffery.smith@wolterskluwer.com',
                   'event_date': '2013-10-11 14:25:00'
                   }

    categories = ['Applications', 'Business Units', 'Locations']

    def setUp(self):
        contact = Contact()
        contact.first_name = "Jeffery"
        contact.last_name = "Smith"
        contact.email = "jeffery.smith@wolterskluwer.com"
        contact.save()
        category = Category(name='Device')
        category.save()
        for category in self.categories:
            Category(name=category).save()

    def test_form_save(self):
        form = EventForm(self.form_values)
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(Event.objects.all().count(), 1)
        event = Event.objects.get(name=self.form_values['name'])
        self.assertEqual(event.tags.all().count(), 2)


class AlertFormTest(TestCase):

    user = DummyObject()
    form_values = {'applications': 'wklmgafjwebfp01,cchnavwebt001',
                   'business_unit': 'taa'}

    def setUp(self):
        self.user.email = lambda: None
        setattr(self.user, 'email',
                'jeffery.smith@wolterskluwer.com')
        contact = Contact(email='jeffery.smith@wolterskluwer.com')
        contact.save()
        category = Category(name='Devices')
        category.save()
        for key in self.form_values.keys():
            category = Category(name=key)
            category.save()

    def test_form_save(self):
        form = AlertForm(self.form_values)
        self.assertTrue(form.is_valid())
        form.save(self.user)
        alert = Alert.objects.get(pk=1)
        self.assertEqual('jeffery.smith@wolterskluwer.com',
                         alert.contact.email)

        tags = alert.tags.all()
        self.assertEqual(tags.count(), 3)
