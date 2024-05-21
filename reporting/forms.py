from django import forms

from reporting.models import MachineVM

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import UserAdmin

HOST_GROUP = (
    "PROD",
    "HORS-PROD",
    "HORS-SUPPORT"
)

ROLE = (
    ("role 1", "Admin RHS"),
    ("role 2", "Admin Nagios"),
    ("role 3", "")
)


class MachineForm(forms.ModelForm):
    class Meta:
        model = MachineVM
        exclude = ["slug", "ip"]


class UploadFileForm(forms.Form):
    csv_file = forms.FileField()


class UserAdminRegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role'].widget = forms.Select(choices=ROLE)

    class Meta:
        model = UserAdmin
        fields = ["first_name", 'last_name', "email", "username"]


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={'placeholder': 'Username'})
        self.fields['password'].widget = forms.PasswordInput(attrs={'placeholder': 'Password'})
