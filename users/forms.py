from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.forms import PasswordInput

from users.apps import UsersConfig
from users.models import CustomUser


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=PasswordInput)

    # def clean_email(self):
    #     email = self.cleaned_data['email']
    #     if not CustomUser.objects.filter(email=email).exists():
    #         raise ValidationError(f'That {email} not found.')
    #     return email
    #
    # def clean_password(self):
    #     password = self.cleaned_data['password']
    #     if not CustomUser.objects.filter(password=password).exists():
    #         raise ValidationError(f'Password did not match')
    #
    # # def clean_password(self):
    # #     password = self.cleaned_data['password']
    # #     if password:
    # #         raise ValidationError(f'Passwords do not match.')
    # #     return password
    #
    # def clean(self):
    #     cleaned_data = super().clean()  # Muhim! Formadagi barcha ma'lumotlarni olish
    #     email = cleaned_data.get("email")
    #     password = cleaned_data.get("password")
    #
    #     if not email or not password:
    #         raise forms.ValidationError("Username or password invalid")
    #
    #     return cleaned_data
