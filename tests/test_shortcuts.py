from django.test.client import RequestFactory
from bullhorn.shortcuts import tags_to_dict, update_model_from_form
from bullhorn.shortcuts import get_query_string, get_model_fields
from bullhorn.shortcuts import process_form, process_contacts, edit_form
from django.test import TestCase
from bullhorn.models import Metadata, Category, Tag, Event, Contact
from bullhorn.forms import EventForm
import datetime


class ShortCutsTest(TestCase):

    categories = ['Device', 'Applications', 'Business Units', 'Locations']
    metatags = ['eStore', 'BizTalk', 'Database', 'PTC-K', 'TAA']

    factory = RequestFactory()
    event_form_data = {'name': 'Test2',
                       'short_description': 'Test2',
                       'description': 'Test2',
                       'event_date': '2009-11-11 00:00:00',
                       'applications': 'icadmin',
                       'contacts': 'jeffery.smith@wolterskluwer.com'}

    def setUp(self):
        for category in self.categories:
            record = Category(name=category)
            record.save()

        for metatag in self.metatags:
            record = Metadata(name=metatag)
            record.save()

        category = Category.objects.all()
        metadata = Metadata.objects.all()
        for i in range(0, 3):
            for meta in metadata:
                tag = Tag(category=category[i],
                          metadata=meta
                          )
                tag.save()

    def test_tags_to_dict(self):
        tags = Tag.objects.all()
        tags_dict = tags_to_dict(tags)
        applications = tags_dict['Applications']
        business_units = tags_dict['Business Units']
        self.assertEqual(applications, "eStore,BizTalk,Database,PTC-K,TAA")
        self.assertEqual(business_units, "eStore,BizTalk,Database,PTC-K,TAA")

    def test_update_model_from_form(self):
        tags = Tag.objects.all()
        dt = datetime.datetime(2013, 10, 11, 12, 41, 00)
        event = Event.objects.create(name='Test1', short_description='Test1',
                                     description='Test1',
                                     event_date=dt.isoformat()
                                     )
        tags = [tag for tag in tags]
        event.tags.add(*tags)
        event_id = event.id
        self.assertTrue(event.tags.all().count() > 1)
        dt = datetime.datetime(2009, 11, 11, 10, 00, 00)
        form = EventForm({'name': 'Test2',
                          'short_description': 'Test2',
                          'description': 'Test2',
                          'contact': 'jeff@wolterskluwer.com',
                          'event_date': '2009-11-11 00:00:00',
                          'applications': 'icadmin',
                          'contacts': 'jeffery.smith@wolterskluwer.com'})
        self.assertTrue(form.is_valid())
        event = update_model_from_form(event, form)
        event = Event.objects.get(pk=event_id)
        self.assertEqual(event.tags.count(), 1)

    def test_get_query_string(self):
        request = self.factory.get('/login?next=frank.html&value=bob123')
        query_values = get_query_string(request)
        self.assertEqual(query_values['next'], 'frank.html')
        self.assertEqual(query_values['value'], 'bob123')
        request = self.factory.get('/login')
        query_values = get_query_string(request)
        self.assertRaises(KeyError, lambda: query_values['next'])

    def test_edit_form(self):
        form_data = self.event_form_data
        form_data['name'] = 'Test Edit Form'
        event = EventForm(form_data)
        event.is_valid()
        event.save()
        event = Event.objects.get(name='Test Edit Form')
        form_data['name'] = 'Test Edit Form 2'
        request = self.factory.post('/event/edit/%s' % event.id, form_data)
        results = edit_form(request, Event, EventForm, event.id)
        self.assertTrue('success_message' in results)

    def test_get_model_fields(self):
        list_of_fields = ('id', 'name', 'short_description', 'description',
                          'event_date')
        list_of_many_to_many = ('contacts', 'tags')
        for event in (Event, Event()):
            fields = get_model_fields(event)
            for field in list_of_fields:
                self.assertTrue(field in fields[0])
            for field in list_of_many_to_many:
                self.assertTrue(field in fields[1])

    def test_process_form(self):
        form_data = self.event_form_data
        form_data['name'] = 'Test3'
        request = self.factory.post('/event/add', self.event_form_data)
        template_variables = process_form(request, EventForm)
        self.assertEqual(template_variables['success_message'],
                         'Record successfully created')
        self.assertEqual(Event.objects.filter(name='Test3').count(), 1)

    def test_process_contacts(self):
        contacts = ['jeffery.smith@wolterskluwer.com', 'jeff@bx.com',
                    'my@fry.com']
        results = process_contacts(contacts)
        self.assertEqual(len(results), 3)
        self.assertEqual(Contact.objects.all().count(), 3)
        results = process_contacts(['jeff@bx.com', 'my@fry.com',
                                    'v@yahoo.com'])
        self.assertEqual(len(results), 3)
        self.assertEqual(Contact.objects.all().count(), 4)
