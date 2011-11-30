from django.template import Context, loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from oa.core.utils import TemplateType
from oa.models import ActiveDirectoryDomain, Application, Location, OperatingSystem,ServerType,Urls,BusinessUnit,ServerEnvironment
from django.http import Http404
from oa.models import DropDownType
import datetime




def getDropDownType(type, getObjects=True):

    ##Return the correct type of object based on what type of application is being used
    ##They all stem from the same object type so once it's returned the interface is the same
    
    if(type == '1'):
       p = ActiveDirectoryDomain

    elif(type == '2'):
        p = Application

    elif(type == '3'):
        p = Location

    elif(type == '4'):
        p = OperatingSystem

    elif(type == '5'):
        p = ServerType

    elif(type == '6'):
        p = Urls

    elif(type == '7'):
        p = BusinessUnit
    elif(type == '8'):
        p = ServerEnvironment

    else:
        p = None

    return p

def list(request, type):

    modelObject = getDropDownType(type)
    t = TemplateType()
    if(type == '1'):
        t.title = "Active Directory Domains"
        t.type = type
    elif(type == '2'):

        t.title = "Applications"
        t.type = type
    elif(type == '3'):
        t.title = "Location Management"
        t.type = type
    elif(type == '4'):
        t.title = "Operating Systems"
        t.type = type
    elif(type == '5'):
        t.title = "Server Types"
        t.type = type
    elif(type == '6'):
        t.title = "URLs"
        t.type = type
    elif(type == '7'):
        t.title = "Business Units"
        t.type = type
    elif(type == '8'):
        t.title = "Server Data Center Environment"
        t.type = type
    else:
        raise Http404

    p = modelObject.objects.all()
    l = loader.get_template('content_list.html')
    c = Context({
            'template': t,
            'records' : p,
            })
    return HttpResponse(l.render(c))


    
def index(request):
    p = DropDownType.objects.all()
    l = loader.get_template('content_index.html')
    c = Context({
            'templates' : p,
            })
    return HttpResponse(l.render(c))

def save(request, type):
    
    import pdb
    pdb.set_trace()
    modelObject = getDropDownType(type)
    p = modelObject()
    p.name = request.POST["nameField"]
    p.description = request.POST["descField"]
    p.save()
    if(request.POST.has_key("response")):
        if(["response"] == "partial"):
            l = loader.get_template('partialDropDown.html')
            c = RequestContext(request, {
                'name' : p.name,
                'desc' : p.description,
                })
            return HttpResponse(l.render(c))
    else:
        return HttpResponseRedirect('/Management/Detail/%s' % type)
    
        
