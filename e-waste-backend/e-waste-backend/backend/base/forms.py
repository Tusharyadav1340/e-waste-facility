from .models import CustomUser
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.validators import RegexValidator

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email','username','password1','password2')


class CustomUserChangeForm(UserChangeForm):
    password = None
    class Meta:
        model = CustomUser
        fields = ('email','username','phone','house','area','landmark','pincode','town','state','country')
        # exclude = ('password',)
        labels = {
            'email': 'Email',
            'username': 'username',
            'phone': 'Phone',
            'house': 'House No,Flat No',
            'area': 'Area',
            'landmark': 'Landmark',
            'pincode': 'Pincode',
            'town': 'Town,City',
            'state': 'State',
            'country': 'Country',
        }

class ChangeDetailForm(UserChangeForm):
    password = None
    class Meta:
        model = CustomUser
        fields = ('username','phone','house','area','landmark','pincode','town','state','country')
        # exclude = ('password',)
        labels = {
            'username': 'username',
            'phone': 'Phone',
            'house': 'House No,Flat No',
            'area': 'Area',
            'landmark': 'Landmark',
            'pincode': 'Pincode',
            'town': 'Town,City',
            'state': 'State',
            'country': 'Country',
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].required = True
