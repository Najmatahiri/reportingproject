import uuid
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User, AbstractUser
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from simple_history.models import HistoricalRecords


# Fichier CSV

class FichierCSV(models.Model):
    # id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=255)
    date_import = models.DateField(auto_now=True)
    contenu = models.FileField(null=False, blank=False, upload_to='csv_files/')


# class Meta:
#     ordering = ['-nom']
#     verbose_name = 'FichierCSV'

# def __str__(self):
#     return self.nom


# Modèle pour les données sur les machines virtuelles

class MachineVM(models.Model):
    id = models.AutoField(primary_key=True)
    modeluuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    history = HistoricalRecords()
    nom_machine = models.CharField(max_length=255, null=False, blank=False, unique=True)
    date_import = models.DateField(auto_now=True, editable=True)
    ip = models.CharField(max_length=255, unique=True)
    group = models.CharField(max_length=100, default="NS")
    os = models.CharField(max_length=255)
    critical = models.IntegerField(null=True, validators=[MinValueValidator(0)])
    important = models.IntegerField(validators=[MinValueValidator(0)])
    moderate = models.IntegerField(validators=[MinValueValidator(0)])
    low = models.IntegerField(validators=[MinValueValidator(0)])

    # fichier_csv = models.ForeignKey('FichierCSV', on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ['-nom_machine']
        verbose_name = 'Inventaire'

    def __str__(self):
        return self.nom_machine

    def get_absolute_url(self):
        return reverse("inventaires")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.modeluuid}{str(self.nom_machine)}")

        super().save(*args, **kwargs)


class ConfigVersionHS(models.Model):
    unsupported_versions = models.CharField(max_length=100, default='')
    history = HistoricalRecords()
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    class Meta:
        verbose_name = 'Configuration'

    def __str__(self):
        return self.unsupported_versions

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.unsupported_versions}")
        super().save(*args, **kwargs)


class UserAdmin(AbstractUser):
    role = models.CharField()
    give_access = models.BooleanField(default=False)
