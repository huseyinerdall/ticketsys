from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm

from .models import User


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(max_length=100, label='Kullanıcı Adı')
    first_name = forms.CharField(max_length=100, label='İsim')
    last_name = forms.CharField(max_length=100, label='Soyisim')

    class Meta:
        model = User
        widgets = {
            'profile_image': forms.FileInput(attrs={'class': 'custom'}),
        }
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2', 'department', 'bio', 'profile_image' )