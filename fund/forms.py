from django import forms
from .models import Fund
from django.forms import ModelForm
from django.contrib.auth.models import User

class FundForm(ModelForm):
    class Meta:
        model = Fund
        fields = '__all__'

class UserForm(forms.Form):  
    username = forms.CharField(label='用户名', max_length=30)
    email = forms.EmailField(label='邮箱地址', max_length=50)
    password = forms.CharField(label='密码', max_length=100,min_length=8,widget=forms.PasswordInput)