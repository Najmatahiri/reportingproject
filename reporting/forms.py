import pandas as pd

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError

from .models import MachineVM, UserAdmin, ConfigVersionHS
from .utils import get_tab_num_hs
import re

# Choices pour les groupes d'hôtes
HOST_GROUP = (
    ("PROD", "PROD"),
    ("Hors-Prod", "Hors-Prod"),
)

# Choices pour les rôles d'utilisateur
ROLE = (
    ("Admin RHS", "Admin RHS"),
    ("Admin Nagios", "Admin Nagios"),
    ("Manager", "Manager")
)


class MachineForm(forms.ModelForm):
    """
    Formulaire pour ajouter ou modifier une machine VM.
    """
    group = forms.ChoiceField(choices=HOST_GROUP)

    def clean_os(self):
        data = self.cleaned_data.get('os')
        pattern = r'^RedHat \d+\.\d+$'
        if not re.match(pattern, data):
            raise ValidationError(
                "Format de système d'exploitation non valide. Il devrait s'agir de « RedHat X.Y » ou « X.Y »."
            )
        return data

    class Meta:
        model = MachineVM
        exclude = ["slug", ]


class UploadFileForm(forms.Form):
    csv_file = forms.FileField()

    def clean_csv_file(self):
        csv_file = self.cleaned_data.get('csv_file')

        # Vérifier l'extension du fichier
        if not csv_file.name.endswith('.csv'):
            raise forms.ValidationError("Le fichier doit être au format CSV.")

        expected_header = ["nom_machine", "ip", "group", "os", "critical", "important", "moderate", "low"]
        expected_length = len(expected_header)

        try:
            # Lire le fichier CSV
            csv_file.seek(0)
            df = pd.read_csv(csv_file)

            # Vérifier et corriger l'en-tête
            if list(df.columns) != expected_header:
                if len(df.columns) != len(expected_header):
                    raise forms.ValidationError(f"L'en-tête du fichier CSV doit avoir {len(expected_header)} colonnes.")
                df.columns = expected_header
                print(df.columns)

            # Vérifier la longueur de chaque ligne et valider les types de données
            for index, row in df.iterrows():
                if len(row) != expected_length:
                    raise forms.ValidationError(f"La ligne {index + 1} n'a pas le bon nombre de colonnes.")
                if not isinstance(row['nom_machine'], str) or not isinstance(row['ip'], str) or \
                        not isinstance(row['os'], str) or \
                        not isinstance(row['critical'], int) or not isinstance(row['important'], int) or \
                        not isinstance(row['moderate'], int) or not isinstance(row['low'], int):
                    raise forms.ValidationError(f"Les types de données de la ligne {index + 1} ne sont pas corrects.")


            # Sauvegarder le DataFrame corrigé dans le champ cleaned_data
            self.cleaned_data['csv_file'] = df
            print(self.cleaned_data['csv_file'])

        except Exception as e:
            raise forms.ValidationError(f"Erreur de lecture du fichier CSV: {str(e)}")

        # Remettre le pointeur du fichier au début après lecture
        csv_file.seek(0)

        return csv_file


# class UploadFileForm(forms.Form):
#     csv_file = forms.FileField()
#
#     def clean_csv_file(self):
#         csv_file = self.cleaned_data.get('csv_file')
#
#         # Vérifier l'extension du fichier
#         if not csv_file.name.endswith('.csv'):
#             print("[+] Le fichier doit être au format CSV.")
#             raise forms.ValidationError("Le fichier doit être au format CSV.")
#
#         # Vérifier l'en-tête du fichier
#         expected_header = ["nom_machine", "ip", "group", "os", "critical", "important", "moderate", "low"]
#
#         try:
#             # Lire le fichier CSV
#             csv_file.seek(0)
#             reader = csv.reader(csv_file.read().decode('utf-8').splitlines())
#             header = next(reader)
#
#             if header != expected_header:
#                 print(f"L'en-tête du fichier CSV doit être {', '.join(expected_header)}.")
#                 raise forms.ValidationError(f"L'en-tête du fichier CSV doit être {', '.join(expected_header)}.")
#         except Exception as e:
#             print(f"Erreur de lecture du fichier CSV: {str(e)}")
#             raise forms.ValidationError(f"Erreur de lecture du fichier CSV: {str(e)}")
#
#         # Remettre le pointeur du fichier au début après lecture
#         csv_file.seek(0)
#
#         return csv_file


# class UploadFileForm(forms.Form):
#     csv_file = forms.FileField()


class UserAdminRegistrationForm(UserCreationForm):
    """
    Formulaire pour l'inscription d'un nouvel administrateur utilisateur.
    """
    role = forms.ChoiceField(choices=ROLE)

    class Meta:
        model = UserAdmin
        fields = ["first_name", 'last_name', "email", "username", 'role']


class LoginForm(AuthenticationForm):
    """
    Formulaire de connexion utilisateur.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={'placeholder': 'Nom d\'utilisateur'})
        self.fields['password'].widget = forms.PasswordInput(attrs={'placeholder': 'Mot de passe'})


class ConfigForm(forms.ModelForm):
    """
    Formulaire pour la configuration des versions non prises en charge.
    """
    unsupported_versions = forms.ChoiceField(
        choices=[],
        widget=forms.Select(attrs={'class': 'styled-select'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.HORS_SUPPORT_LIST = (
            (f"RedHat {i}", f"RedHat {i}")
            for i in range(5, 100) if i not in get_tab_num_hs()
        )
        self.fields['unsupported_versions'].choices = self.HORS_SUPPORT_LIST

    class Meta:
        model = ConfigVersionHS
        fields = ["unsupported_versions"]
