# Create your views here.
from django.template import Context, RequestContext
from django.http import HttpResponse
from django.shortcuts import render_to_response


def index(request):
    return render_to_response('index.html',
                              context_instance=RequestContext(request))


def add_node(request):
    pass

