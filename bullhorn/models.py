from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200, blank=True)


class Metadata(models.Model):
    name = models.CharField(max_length=200)


class Tag(models.Model):
    metadata = models.ForeignKey(Metadata)
    category = models.ForeignKey(Category)
    parent = models.ForeignKey(Metadata, related_name='parent', blank=True,
                               null=True)


class Node(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    tags = models.ManyToManyField(Tag, blank=True)

    def add_tag(self, tag=None, metadata=None, category=None, parent=None):
        if not tag and (not metadata or not category):
            raise ValueError("Not valid")
        if not tag:
            metadata_object = Metadata.objects.get_or_create(name=metadata)
            category_object = Category.objects.get_or_create(name=category)
            if parent:
                parent_object = Metadata.objects.get_or_create(name=parent)
            else:
                parent_object = (None,)
            tag = Tag(metadata=metadata_object[0],
                      category=category_object[0], parent=parent_object[0])
        tag.save()
        self.save()
        self.tags.add(tag)

    def remove_tag(self, tag):
        self.tags.remove(tag)


class Contact(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=75)
    office = models.CharField(max_length=10, null=True, blank=True)
    mobile = models.CharField(max_length=10, null=True, blank=True)
    instant_message = models.CharField(max_length=50, blank=True)


class Event(models.Model):
    name = models.CharField(max_length=200)
    short_description = models.CharField(max_length=500)
    description = models.TextField()
    tags = models.ManyToManyField(Metadata, null=True, blank=True)
    contacts = models.ManyToManyField(Contact, null=True, blank=True)
    event_date = models.DateTimeField()
    create_date = models.DateTimeField(auto_now=True)
