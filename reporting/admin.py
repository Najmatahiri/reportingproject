from django.contrib import admin
from reporting.models import MachineVM, FichierCSV
from import_export.admin import ImportExportModelAdmin
from .ressources import MachineVMResource


class MachineVMAdmin(ImportExportModelAdmin):
    resource_classes = [MachineVMResource]
    list_display = ('nom_machine', 'ip', 'group', 'os', 'critical', 'date_import')
    exclude = ("id",)


admin.site.register(MachineVM, MachineVMAdmin)

@admin.register(FichierCSV)
class FichierCSVAdmin(admin.ModelAdmin):
    list_display = ['nom', 'contenu', 'date_import']


