from django.test import TestCase
from reporting.models import MachineVM


class TestMachineVM(TestCase):
    def setUp(self):
        self.machinevm = MachineVM.objects.create(
            nom_machine="test_machine",
            ip="127.0.0.1",
            group="PROD",
            os="RedHat 8.7",
            critical=0,
            important=10,
            moderate=14,
            low=8,

        )