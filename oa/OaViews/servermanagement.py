from django.template import Context, loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from oa.forms.management import *
from django.shortcuts import render_to_response

def add(request):
    form = ServerCreationForm()
    return render_to_response("serveradd.html", { 'form' : form }, 
                              context_instance=RequestContext(request))
    
    
