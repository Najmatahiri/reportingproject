# Generated by Django 5.0.6 on 2024-06-04 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reporting', '0008_historicalconfigversionhs_historicalmachinevm'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='configversionhs',
            options={'verbose_name': 'Configuration'},
        ),
        migrations.AlterModelOptions(
            name='historicalconfigversionhs',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical Configuration', 'verbose_name_plural': 'historical Configurations'},
        ),
        migrations.AddField(
            model_name='historicalmachinevm',
            name='import_month',
            field=models.CharField(default='15', editable=False, max_length=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='historicalmachinevm',
            name='import_year',
            field=models.CharField(default='2024', editable=False, max_length=4),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='machinevm',
            name='import_month',
            field=models.CharField(default='06', editable=False, max_length=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='machinevm',
            name='import_year',
            field=models.CharField(default='2024', editable=False, max_length=4),
            preserve_default=False,
        ),
    ]