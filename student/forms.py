from django.forms import ModelForm
from .models import Input
from django import forms

from django.contrib.admin.widgets import AdminDateWidget
from django.forms.fields import DateField


class InputForm(ModelForm):
    class Meta:
        model = Input
        fields = ['source', 'destination', 'date']

"""class InForm(forms.Form):
    source = forms.CharField(label='')
    destination = forms.CharField(initial='london')"""
