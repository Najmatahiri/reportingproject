import pandas as pd
import tablib
from django.urls import reverse_lazy

from django.db.models import Sum
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView, FormView, MonthArchiveView

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from reporting.models import MachineVM, FichierCSV

from .forms import MachineForm, UploadFileForm
from rest_framework.views import APIView
from rest_framework.response import Response
from reporting.serializers import MachineVMSerializer
from tablib import Dataset
from .ressources import MachineVMResource


def index(request):
    return render(request, 'reporting/home.html', context={'nom': "Abdoul Bassit"})


# Importer un fichier csv


class ImportCSV(FormView):
    template_name = 'reporting/import_csv.html'
    form_class = UploadFileForm
    success_url = reverse_lazy("inventaires")

    def form_valid(self, form):
        fichier_csv = form.cleaned_data['csv_file']
        df = pd.read_csv(fichier_csv)
        print(df)
        dataset = Dataset().load(df)
        print(dataset)
        machinevm_resource = MachineVMResource()
        result = machinevm_resource.import_data(dataset, dry_run=True, raise_errors=True)
        if not result.has_errors():
            result = machinevm_resource.import_data(dataset, dry_run=False)
            print(result)
            return HttpResponseRedirect(self.get_success_url())

        return HttpResponse("<h1> Erreur lors de l'importation</h1>")


class Dashboard(ListView):
    model = MachineVM
    template_name = 'reporting/dashboard/dashboard.html'
    context_object_name = 'inventaires'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        somme_patchs = MachineVM.objects.aggregate(
            total_critical=Sum("critical"),
            total_important=Sum("important"),
            total_moderate=Sum("moderate"),
            total_low=Sum("low"),
        )
        context['somme_patchs'] = somme_patchs
        return context


class InventaireView(ListView):
    model = MachineVM
    template_name = 'reporting/inventaires/inventaires.html'
    context_object_name = 'inventaires'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nb_patched"] = MachineVM.objects.filter(critical__gt=0).count()
        context["total_machine"] = MachineVM.objects.all().count()
        return context


class MachineUpdateView(UpdateView):
    model = MachineVM
    form_class = MachineForm
    template_name = 'reporting/machinevm/update_vm.html'
    context_object_name = "vm"
    success_url = reverse_lazy("inventaires")


class MachineDetailView(DetailView):
    model = MachineVM
    template_name = 'reporting/machinevm/machine_vm_details_view.html'
    context_object_name = "vm"


class MachineDeleteView(DeleteView):
    model = MachineVM
    template_name = 'reporting/machinevm/delete_vm.html'
    context_object_name = "vm"
    success_url = reverse_lazy("inventaires")


class MachineVMAPIView(APIView):

    def get(self, *args, **kwargs):
        machines = MachineVM.objects.all()
        serializer = MachineVMSerializer(machines, many=True)
        return Response(serializer.data)


class MachineVMViewSet(ModelViewSet):
    serializer_class = MachineVMSerializer

    def get_queryset(self):
        return MachineVM.objects.all()


class MachineArchiveView(MonthArchiveView):
    model = MachineVM
    date_field = 'date_import'
    template_name = 'reporting/inventaires/machine_archive.html'
    context_object_name = 'machines'
    pass
    # Définissez les propriétés ici, telles que :
    # - model (le modèle de données que vous interrogez)
    # - date_field (le champ de votre modèle qui stocke la date)
    # - template_name (le fichier de modèle utilisé pour rendre la vue)
    # - context_object_name (le nom utilisé pour accéder aux données dans le modèle)
