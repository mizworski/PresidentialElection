from django import forms

MAX_PASS_LENGTH = 32
MAX_LOGIN_LENGTH = 32


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=MAX_LOGIN_LENGTH)
    password = forms.CharField(max_length=MAX_PASS_LENGTH)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=MAX_LOGIN_LENGTH)
    password = forms.CharField(max_length=MAX_PASS_LENGTH)


class UpdateForm(forms.Form):
    def __init__(self, field_names, *args, **kwargs):
        super(UpdateForm, self).__init__(*args, **kwargs)
        for field_name in field_names:
            self.fields[field_name] = forms.IntegerField(required=False)
