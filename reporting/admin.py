from django.contrib import admin

from reporting.models import MachineVM, UserAdmin, ConfigVersionHS
from import_export.admin import ImportExportModelAdmin
from .ressources import MachineVMResource
from simple_history.admin import SimpleHistoryAdmin


@admin.register(MachineVM)
class MachineVMAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):
    resource_classes = [MachineVMResource]
    list_display = ('nom_machine', 'ip', 'group', 'os', 'critical', 'date_import')
    history_list_display = ('nom_machine', 'ip', 'group', 'os', 'critical', 'date_import')
    exclude = (" id", "slug")


@admin.register(UserAdmin)
class UserAdminAdmin(admin.ModelAdmin):
    pass


@admin.register(ConfigVersionHS)
class ConfigAdmin(SimpleHistoryAdmin):
    fields = ["unsupported_versions"]
    history_list_display = ["unsupported_versions"]

# @admin.register(FichierCSV)
# class FichierCSVAdmin(admin.ModelAdmin):
#     list_display = ['nom', 'contenu', 'date_import']
