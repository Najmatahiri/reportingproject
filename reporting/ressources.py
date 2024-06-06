from datetime import datetime

from import_export import resources
from .models import MachineVM


class MachineVMResource(resources.ModelResource):

    class Meta:
        model = MachineVM
        # import_id_fields = ("ip", "import_month", "import_year")
        import_id_fields = ("nom_machine", "import_month", "import_year")
        skip_unchanged = True
        report_skipped = False
        update_existing = True

        # exclude = ('id',"date_import", "slug")

