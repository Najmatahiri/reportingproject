from django import forms

HOST_GROUP = (
    "PROD",
    "HORS-PROD",
    "HORS-SUPPORT"
)


class MachineForm(forms.Form):
    host = forms.CharField(max_length=50, required=True)
    ip = forms.CharField(max_length=16, required=True)
    group = forms.ChoiceField(choices=HOST_GROUP, required=True, widget=forms.RadioSelect())
    operating_system = forms.CharField(max_length=80)
    critical = forms.IntegerField()
    important = forms.IntegerField()
    moderate = forms.IntegerField()
    low = forms.IntegerField()


class FileCSVImportForm(forms.Form):
    fichier_csv = forms.FileField(help_text="Sélectionner le fichier csv à importer", label='', widget=forms.FileInput(attrs={"class": "input_csv"}))
