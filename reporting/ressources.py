from import_export import resources

from .models import MachineVM


class MachineVMResource(resources.ModelResource):
    class Meta:
        model = MachineVM
        import_id_fields = ("ip",)
        skip_unchanged = True
        report_skipped = False
        # exclude = ('id',"date_import", "slug")

