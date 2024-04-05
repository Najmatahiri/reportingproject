from django import forms

from reporting.models import MachineVM

from django.contrib.auth.forms import UserCreationForm

from .models import UserAdmin

HOST_GROUP = (
    "PROD",
    "HORS-PROD",
    "HORS-SUPPORT"
)

ROLE = (
    ("ADMIN RSH", "Admin RHS"),
    ("admin NAGIOS", "Admin Nagios"),
)


class MachineForm(forms.ModelForm):
    class Meta:
        model = MachineVM
        exclude = ["slug", "ip"]


class UploadFileForm(forms.Form):
    csv_file = forms.FileField()


class UserAdminRegistrationForm(UserCreationForm):
    class Meta:
        model = UserAdmin
        fields = ["email","username"]
        widgets = {
            "role": forms.RadioSelect(choices=ROLE)
        },


