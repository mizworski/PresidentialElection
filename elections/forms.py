from django import forms

MAX_PASS_LENGTH = 32
MAX_LOGIN_LENGTH = 32


class RegisterForm(forms.Form):
    login = forms.CharField(max_length=MAX_LOGIN_LENGTH)
    password = forms.CharField(max_length=MAX_PASS_LENGTH)
    password_repeat = forms.CharField(max_length=MAX_PASS_LENGTH)


class LoginForm(forms.Form):
    login = forms.CharField(max_length=MAX_LOGIN_LENGTH)
    password = forms.CharField(max_length=MAX_PASS_LENGTH)
