import uuid

from django.urls import reverse
from reporting.models import MachineVM, UserAdmin
from django.test import TestCase, Client


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = UserAdmin.objects.create_user(username="test_username2", password="123456", give_access=True)

        self.dashboard_url = reverse('dashboard')
        self.inventaire_url = reverse('inventaires')

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

        self.importCSV_url = reverse('importer')

    def test_dashboard_GET(self):
        self.client.login(username="test_username2", password="123456")
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reporting/dashboard/dashboard.html')

    def test_inventaires_GET(self):
        self.client.login(username="test_username2", password="123456")
        response = self.client.get(self.inventaire_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reporting/inventaires/inventaires.html')

    def test_importfile_GET(self):
        self.client.login(username="test_username2", password="123456")
        response = self.client.get(self.importCSV_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reporting/utils/import_csv.html')

    def test_machineUpdate_UPDATE(self):
        self.client.login(username="test_username2", password="123456")
        response = self.client.post(self.machine_update_url, data={"machine": "test_machine_update"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reporting/machinevm/update_vm.html')

    def test_machineDelete_DELETE(self):
        self.client.login(username="test_username2", password="123456")
        response = self.client.post(self.machine_delete_url)
        self.assertRedirects(response, self.inventaire_url)
