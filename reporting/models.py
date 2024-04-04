import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify


User = get_user_model()


# Fichier CSV

class FichierCSV(models.Model):
    # id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=255)
    date_import = models.DateField(auto_now=True)
    file_author = models.ForeignKey(User, models.SET_NULL, null=True, blank=True)
    contenu = models.FileField(null=False, blank=False, upload_to='csv_files/')

    class Meta:
        ordering = ['-nom']
        verbose_name = 'FichierCSV'

    def __str__(self):
        return self.nom


# Modèle pour les données sur les machines virtuelles

class MachineVM(models.Model):
    id = models.AutoField(primary_key=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    nom_machine = models.CharField(max_length=255, null=False, blank=False, unique=True)
    date_import = models.DateField()
    ip = models.CharField(max_length=255, unique=True)
    group = models.CharField(max_length=100)
    os = models.CharField(max_length=255)
    critical = models.IntegerField()
    important = models.IntegerField()
    moderate = models.IntegerField()
    low = models.IntegerField()
    # fichier_csv = models.ForeignKey('FichierCSV', on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ['-nom_machine']
        verbose_name = 'Inventaire'


    def __str__(self):
        return self.nom_machine

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom_machine)
        super().save(*args, **kwargs)

    def is_patched(self):
        if self.critical == 0:
            return True
        return False

