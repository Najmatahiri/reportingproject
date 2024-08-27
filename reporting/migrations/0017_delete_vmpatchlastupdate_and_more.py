# Generated by Django 5.0.6 on 2024-07-22 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reporting', '0016_vmpatchlastupdate'),
    ]

    operations = [
        migrations.DeleteModel(
            name='VMPatchLastUpdate',
        ),
        migrations.AlterField(
            model_name='historicalmachinevm',
            name='date_import',
            field=models.DateTimeField(blank=True, editable=False),
        ),
        migrations.AlterField(
            model_name='machinevm',
            name='date_import',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
