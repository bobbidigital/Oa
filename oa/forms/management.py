from django import forms
from oa.models import *

class ModelLookupField(forms.ModelChoiceField):
    #def __init__(self, queryset=None, empty_label=None):
    #    super(ModelLookupField, self)
    def label_from_instance(self, obj):
        return "%s" % obj.name

class ModelMultipleLookupField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return "%s" % obj.name

class ServerCreationForm(forms.Form):

    server_name = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)
    location = ModelLookupField(queryset=Location.objects.all(), empty_label="Please Select")
    operating_system = ModelLookupField(queryset=OperatingSystem.objects.all(), empty_label="Please Select")
    business_unit = ModelLookupField(queryset=BusinessUnit.objects.all(), empty_label="Please Select")
    server_environment = ModelLookupField(queryset=ServerEnvironment.objects.all(), empty_label="Please Select")
    applications = ModelMultipleLookupField(queryset=Application.objects.all(), widget=forms.CheckboxSelectMultiple)
    urls = ModelMultipleLookupField(queryset=Urls.objects.all(), widget=forms.CheckboxSelectMultiple)
    ad_domains = ModelMultipleLookupField(queryset=ActiveDirectoryDomain.objects.all(), widget=forms.CheckboxSelectMultiple)
    ip_post = forms.MultipleHiddenInput()
    ip = forms.MultiValueField(widget=forms.MultiWidget(widgets=(forms.TextInput, forms.TextInput)))
