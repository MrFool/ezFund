from django import forms
from .models import Fund
from django.forms import ModelForm

class FundForm(ModelForm):
    class Meta:
        model = Fund
        fields = '__all__'