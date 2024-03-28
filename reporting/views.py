import csv
import pandas as pd
from django.urls import reverse, reverse_lazy

from django.db.models import Sum, Min
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView, FormView

from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from reporting.models import MachineVM, FichierCSV

from .forms import MachineForm, FileCSVImportForm
from rest_framework.views import APIView
from rest_framework.response import Response
from reporting.serializers import MachineVMSerializer
from tablib import Dataset
from .ressources import MachineVMResource


# Create your views here.

def index(request):
    return render(request, 'reporting/home.html', context={'nom': "Abdoul Bassit"})


# Importer un fichier csv


class ImportCSV(TemplateView):
    template_name = 'reporting/import_csv.html'

    def post(self, request, *args, **kwargs):
        fichier_csv = request.FILES['fichier_csv']
        df = pd.read_csv(fichier_csv)
        print(df)
        # Load the pandas dataframe into a tablib dataset
        dataset = Dataset().load(df)
        print(dataset)
        # Call the machine Resource Model and make its instance
        machinevm_resource = MachineVMResource()
        # Call the import_data hook and pass the tablib dataset
        result = machinevm_resource.import_data(dataset,dry_run=True, raise_errors=True)

        if not result.has_errors():
            result = machinevm_resource.import_data(dataset, dry_run=False)
            return render(request, "reporting/success_import.html")

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
        return context


class MachineUpdate(UpdateView):
    model = MachineVM
    form_class = MachineForm
    template_name = 'reporting/upadate_vm.html'
    context_object_name = "vm"


class MachineVMAPIView(APIView):

    def get(self, *args, **kwargs):
        machines = MachineVM.objects.all()
        serializer = MachineVMSerializer(machines, many=True)
        return Response(serializer.data)


class MachineVMViewset(ReadOnlyModelViewSet):
    serializer_class = MachineVMSerializer

    def get_queryset(self):
        return MachineVM.objects.all()
