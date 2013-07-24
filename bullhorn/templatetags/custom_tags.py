from django.core.serializers import serialize
from django.db.models.query import QuerySet
from django.template import Library
from django.utils import simplejson
import json

register = Library()

# Found on Django Snippets
# http://djangosnippets.org/snippets/201/


def jsonify(object):
    if isinstance(object, QuerySet):
        return serialize('json', object)
    return simplejson.dumps(object)


def jsonify_list(data):
    metadata = {meta: meta for meta in data}
    return simplejson.dumps(metadata)


def js_array(data):
    metadata = [x for x in data]
    return json.dumps(metadata)

register.filter('jsonify', jsonify)
register.filter('jsonify_list', jsonify_list)
register.filter('js_array', js_array)
