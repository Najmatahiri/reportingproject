from django import forms

from reporting.models import MachineVM

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import UserAdmin, ConfigVersionHS

HOST_GROUP = (
    ("PROD", "PROD",),
    ("Hors-Prod","Hors-Prod"),
)

ROLE = (
    ("role 1", "Admin RHS"),
    ("role 2", "Admin Nagios"),
    ("role 3", "Visiteur")
)



class MachineForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['group'].widget = forms.Select(choices=HOST_GROUP)

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
        fields = ["first_name", 'last_name', "email", "username", 'role']


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={'placeholder': 'Username'})
        self.fields['password'].widget = forms.PasswordInput(attrs={'placeholder': 'Password'})


class ConfigForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['unsupported_versions'].widget = forms.Select(choices=HORS_SUPPORT_LIST)

    class Meta:
        model = ConfigVersionHS
        fields = ["unsupported_versions"]
