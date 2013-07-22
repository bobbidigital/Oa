from bullhorn.shortcuts import tags_to_dict, update_model_from_form
from django.test import TestCase
from bullhorn.models import Metadata, Category, Tag, Event
from bullhorn.forms import EventForm
import datetime


class ShortCutsTest(TestCase):

    categories = ['Device', 'Applications', 'Business Units', 'Locations']
    metatags = ['eStore', 'BizTalk', 'Database', 'PTC-K', 'TAA']

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
                                     #event_date='2013-10-11 12:4l:00'
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
