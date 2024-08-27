from .models import MachineVM
from datetime import datetime
month = datetime.today().strftime('%m')
year = datetime.today().strftime('%Y')
MachineVM.objects.filter(import_month=month, import_year=year).first()