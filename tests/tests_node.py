"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from bullhorn.models import Node, Tag, Metadata, Category


class NodeTest(TestCase):

    categories = ['Applications', 'Business Units', 'Locations']
    metatags = ['eStore', 'BizTalk', 'Database', 'PTC-K', 'TAA']

    def setUp(self):
        for category in self.categories:
            record = Category(name=category)
            record.save()

        for metatag in self.metatags:
            record = Metadata(name=metatag)
            record.save()

    def test_add_tag(self):
        node = Node(name='WKCLSBIZTALBT03')
        meta = Metadata.objects.filter(name='eStore')
        category = Category.objects.filter(name='Applications')
        tag = Tag(metadata=meta[0], category=category[0])
        node.add_tag(tag)
        db_tag = Tag.objects.get(pk=1)
        self.assertEqual(tag, db_tag)

    def test_add_tag_params(self):
        node = Node(name='WKCLSBIZTALBT04')
        meta = Metadata.objects.get(name='TAA')
        category = Category.objects.get(name='Business Units')
        node.add_tag(metadata='TAA', category='Business Units')
        db_tag = Tag.objects.get(metadata__name=meta.name,
                                 category__name=category.name)
        self.assertEqual(db_tag.metadata.name, meta.name)
        self.assertEqual(db_tag.category.name, category.name)

    def test_remove_tag(self):
        node = Node(name='JeffTest')
        node.add_tag(metadata='Franklin', category='PTC-K')
        tags = node.tags.all()
        self.assertEqual(tags[0].metadata.name, 'Franklin')
        node.remove_tag(tags[0])
        node = Node.objects.get(name='JeffTest')
        self.assertEqual(len(node.tags.all()), 0)
