from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import ExtendedUser


class UserCreationWithEmailForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')
    class Meta:
        model = get_user_model()
        fields = ("username", "email")

class GoogleUserChangeUsername(forms.ModelForm):
    username = forms.CharField(required=True, label='Username')
    class Meta:
        model = get_user_model()
        fields = ("username",)


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
