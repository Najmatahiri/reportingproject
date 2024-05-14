from django.test import SimpleTestCase, TestCase, Client
from django.urls import reverse, resolve

from reporting.models import MachineVM
from reporting.views import Dashboard, InventaireView, ImportCSV, MachineDetailView, MachineUpdateView, MachineDeleteView


class TestUrls(TestCase):

    def setUp(self):
        self.dashboard_url = reverse("dashboard")
        self.inventaire_url = reverse("inventaires")
        self.importCSV_url = reverse("importer")

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
        self.machine_update_url = reverse('update-vm', kwargs={'slug': self.machinevm.slug})
        self.machine_delete_url = reverse('delete-vm', kwargs={'slug': self.machinevm.slug})

    def test_dashboard_url_is_resolved(self):
        url = self.dashboard_url
        self.assertEqual(resolve(url).func.view_class, Dashboard)

    def test_inventaire_url_is_resolved(self):
        url = self.inventaire_url
        self.assertEqual(resolve(url).func.view_class, InventaireView)

    def test_importCSV_url_is_resolved(self):
        url = self.importCSV_url
        self.assertEqual(resolve(url).func.view_class, ImportCSV)

    def test_machineUpdate_url_is_resolved(self):
        url = self.machine_update_url
        self.assertEqual(resolve(url).func.view_class, MachineUpdateView)

    def test_machineDelete_url_is_resolved(self):
        url = self.machine_delete_url
        self.assertEqual(resolve(url).func.view_class, MachineDeleteView)

