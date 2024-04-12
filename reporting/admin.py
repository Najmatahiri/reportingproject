from django.contrib import admin
from reporting.models import MachineVM, UserAdmin
from import_export.admin import ImportExportModelAdmin
from .ressources import MachineVMResource


class MachineVMAdmin(ImportExportModelAdmin):
    resource_classes = [MachineVMResource]
    list_display = ('nom_machine', 'ip', 'group', 'os', 'critical', 'date_import')
    exclude = (" id", "slug")


admin.site.register(MachineVM, MachineVMAdmin)


@admin.register(UserAdmin)
class UserAdminAdmin(admin.ModelAdmin):
    pass

# @admin.register(FichierCSV)
# class FichierCSVAdmin(admin.ModelAdmin):
#     list_display = ['nom', 'contenu', 'date_import']
