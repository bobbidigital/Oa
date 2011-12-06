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

    try:
        dropdown = DropDownType.objects.get(pk=type)
    except:
        p = None
        return p
   
    if(dropdown.name == 'Active Directory Domains'):
       p = ActiveDirectoryDomain

    elif(dropdown.name == 'Application'):
        p = Application

    elif(dropdown.name == 'Location'):
        p = Location

    elif(dropdown.name == 'Operating Systems'):
        p = OperatingSystem

    elif(dropdown.name == 'Server Types'):
        p = ServerType

    elif(dropdown.name == 'URLs'):
        p = Urls

    elif(dropdown.name == 'Business Unit'):
        p = BusinessUnit

    elif(dropdown.name == 'Server Environment'):
        p = ServerEnvironment

    else:
        p = None

    return p

def list(request, type):
    ##To make this function generic, first we figure out what type of model we're working with
    modelObject = getDropDownType(type)
    t = TemplateType()
    
    #Now let's get the specifc entry we're looking for the type will always be equal to the ID
    # of the entry. 

    try:
        p = DropDownType.objects.get(pk=type)
    except:
        raise Http404
    
    #Our template object will allow us to use a single template for all of these management
    #dropdowns. Let's just assign a title and the type

    t.title = p.name
    t.type = type
   
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

def save(request):
    type = request.POST["template"]
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
        return list(request,type)
        
        
    
        
