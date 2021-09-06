  
from django import forms
from django.db.models import fields
from .models import *

class ProdForm(forms.ModelForm):

    class Meta:
        model = product
        fields = '__all__'

class calcFret(forms.Form):
    cep = forms.CharField(label=False ,max_length=100)