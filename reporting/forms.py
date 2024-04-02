from django import forms

from reporting.models import MachineVM

HOST_GROUP = (
    "PROD",
    "HORS-PROD",
    "HORS-SUPPORT"
)


class MachineForm(forms.ModelForm):
    class Meta:
        model = MachineVM
        exclude = ["slug", "ip"]


class UploadFileForm(forms.Form):
    csv_file = forms.FileField()
