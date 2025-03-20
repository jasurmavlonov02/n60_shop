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


class RegisterModelForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'confirm_password')

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError(f'This {email} already registered.')
        return email

    def clean_confirm_password(self):
        confirm_password = self.cleaned_data.get('confirm_password')
        password = self.cleaned_data.get('password')
        if password != confirm_password:
            raise forms.ValidationError(f'Password don\'t match')
        return confirm_password


