from django.db import models

# Create your models here.

class CommonObject(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500)

    class Meta:
        abstract = True

class ActiveDirectoryDomain(CommonObject):
    pass

class Application(CommonObject):
    pass

class Location(CommonObject):
    pass

class OperatingSystem(CommonObject):
    pass

class ServerType(CommonObject):
    pass

class Urls(CommonObject):
    pass

class BusinessUnit(CommonObject):
    pass

class ServerEnvironment(CommonObject):
    pass

class IPAddress(models.Model):
    address = models.IPAddressField()
    subnet = models.IPAddressField()
    

class Server(models.Model):
    hostname = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    location = models.ForeignKey(Location)
    operating_system = models.ForeignKey(OperatingSystem)
    business_unit = models.ForeignKey(BusinessUnit)
    server_environment = models.ForeignKey(ServerEnvironment)
    urls = models.ManyToManyField(Urls)
    addresses = models.ManyToManyField(IPAddress)
    applications = models.ManyToManyField(Application)
    active_directory_domains = models.ManyToManyField(ActiveDirectoryDomain)
    server_types = models.ManyToManyField(ServerType)

class DropDownType(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
