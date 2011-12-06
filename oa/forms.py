from django import forms
from oa.Models import *

class ServerForm(forms.Form):
    
    hostname = forms.CharField(max_length=200, required=True)
    location = forms.ModelChoiceField(queryset = Location.objects.all(), widget=forms.Select)
    os = forms.ModelChoiceField(queryset = OperatingSystem.objects.all(), widget=forms.Select)
    business_unit = forms.ModelChoiceField(queryset = BusinessUnit.objects.all(), widget=forms.Select)
    server_environment = forms.ModelChoiceField(queryset = ServerEnvironment.objects.all(), widget=forms.Select)
    application = forms.ModelChoiceField(queryset = Application.objects.all(), widget=forms.Checkboxinput)
    active_directory = forms.ModelChoiceField(queryset = ActiveDirectoryDomain.objects.all, widget=forms.Checkboxinput)
    
