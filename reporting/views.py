import io
import os
from datetime import datetime

import pandas as pd
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.utils.decorators import method_decorator
from django.views.generic import ListView, UpdateView, DetailView, DeleteView, FormView, TemplateView, CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from django.contrib.auth.decorators import login_required
from reporting.models import MachineVM, ConfigVersionHS
from reportingauto import settings
from .forms import MachineForm, UploadFileForm, UserAdminRegistrationForm, LoginForm, ConfigForm
from reporting.serializers import MachineVMSerializer, ConfigVersionHSSerializer
from tablib import Dataset
from .ressources import MachineVMResource
from .decorators import access_required, role_required
from reportingauto.settings import EMAIL_HOST_USER, BASE_DIR
from django.http import FileResponse
from .utils_pdf import create_pdf_buffer
from .utils import get_lit_out_of_support, get_list_in_support, month_year
from pathlib import Path

temporary_file_folder = BASE_DIR / 'temporary_files'
if not os.path.exists(temporary_file_folder):
    os.makedirs(temporary_file_folder)


def signup(request):
    if request.method == "POST":
        form = UserAdminRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("index")
    else:
        form = UserAdminRegistrationForm()

    return render(request, "accounts/signup.html", context={"form": form})


@login_required
def index(request):
    if request.user.give_access:
        return redirect("dashboard")
    else:
        return render(request, "reporting/utils/home.html")


def landing_page(request):
    return render(request, "landing_page.html")


def handler404(request, exception):
    return render(request, '404.html', status=404)


def handler500(request):
    return render(request, '500.html', status=500)


def access_denied(request):
    return render(request, 'access_denied.html')


def send_welcome_email(request):
    subject = 'Welcome to My Site'
    message = 'Thank you for creating an account!'
    from_email = EMAIL_HOST_USER
    recipient_list = ['abdelbassitalamine@gmail.com']
    send_mail(subject, message, from_email, recipient_list)
    return HttpResponse("<h1>Le message a été bien envoyé</h1>")


def logout_view(request):
    year = month_year()[1]
    return render(request, 'logout_page.html')


# Importer un fichier csv
@method_decorator(access_required, name='dispatch')
@method_decorator(login_required, name="dispatch")
@method_decorator(role_required("Admin RHS"), name='dispatch')
class ImportCSV(FormView):
    template_name = 'reporting/utils/import_csv.html'
    form_class = UploadFileForm
    success_url = reverse_lazy("inventaires")

    def form_valid(self, form):
        expected_header = ["nom_machine", "ip", "group", "os", "critical", "important", "moderate", "low"]
        try:
            fichier_csv = form.cleaned_data['csv_file']
            # Lire le fichier CSV
            df = pd.read_csv(fichier_csv)
            df.columns = expected_header

            # Ajouter les champs month_import et year_import
            current_date = datetime.now()
            import_month = current_date.strftime('%m')
            import_year = current_date.strftime('%Y')
            df['import_month'] = import_month
            df['import_year'] = import_year

            # Sauvegarder le fichier modifié dans le répertoire temporaire
            modified_csv_path = os.path.join(temporary_file_folder, 'modified_import.csv')
            df.to_csv(modified_csv_path, index=False)

            # verifcation
            with open(modified_csv_path, 'r') as file:
                first_line = file.readline()
                print(f"En-têtes du fichier modifié: {first_line.strip()}")

            # Importer les données du fichier CSV modifié par chunks

            df1 = pd.read_csv(modified_csv_path,  dtype={"nom_machine": str, "import_month": str, "import_year": str})
            dataset = Dataset().load(df1)
            machinevm_resource = MachineVMResource()
            result = machinevm_resource.import_data(dataset, dry_run=True, raise_errors=True)
            if not result.has_errors():
                MachineVM.objects.filter(import_month=import_month, import_year=import_year).delete()
                machinevm_resource.import_data(dataset, dry_run=False)
            else:
                raise Exception("Erreur lors de l'importation")

            # chunk_size = 500
            # for chunk in pd.read_csv(modified_csv_path, chunksize=chunk_size,
            #                          dtype={"nom_machine": str, "import_month": str, "import_year": str}):
            #     dataset = Dataset().load(chunk)
            #     machinevm_resource = MachineVMResource()
            #     result = machinevm_resource.import_data(dataset, dry_run=True, raise_errors=True)
            #     if not result.has_errors():
            #         machinevm_resource.import_data(dataset, dry_run=False)
            #     else:
            #         raise Exception("Erreur lors de l'importation")
            print(df1)
            print("Fichier importé avec succès")

            return super().form_valid(form)
        except Exception as e:
            print(e)
            return self.render_to_response(self.get_context_data(form=form, error=str(e)))
        finally:
            # Supprimer le fichier temporaire
            if os.path.exists(modified_csv_path):
                os.remove(modified_csv_path)


@method_decorator(access_required, name='dispatch')
@method_decorator(role_required("Admin RHS", "Manager"), name='dispatch')
class Dashboard(ListView):
    model = MachineVM
    template_name = 'reporting/dashboard/dashboard.html'
    context_object_name = 'inventaires'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        top_20 = get_list_in_support("critical")[:20]
        machine_hs_filtre = get_lit_out_of_support()
        total_hs = len(machine_hs_filtre)
        current_username = self.request.user.username
        role = self.request.user.role
        context["role"] = role
        context['username'] = current_username
        # context['list_role'] = ["Admin RHS", "Manager"]
        context['top_20'] = top_20
        context['machine_hs'] = machine_hs_filtre
        context['is_in_list_permitted_rhs'] = role in ["Admin RHS", "Manager"]
        context["is_admin_rhs"] = role == "Admin RHS"
        context['total_hs'] = total_hs
        return context


@method_decorator(role_required("Admin RHS"), name='dispatch')
class InventaireView(ListView):
    model = MachineVM
    template_name = 'reporting/inventaires/inventaires.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_machine"] = MachineVM.objects.all().filter(
            import_month=month_year()[0],
            import_year=month_year()[1]
        ).count()

        role = self.request.user.role
        context["role"] = role
        context['is_in_list_permitted_rhs'] = role in ["Admin RHS", "Manager"]
        context["is_admin_rhs"] = role == "Admin RHS"
        context['inventaires'] = get_list_in_support()
        return context


@method_decorator(role_required("Admin RHS"), name='dispatch')
class MachineCreateView(CreateView):
    model = MachineVM
    form_class = MachineForm
    template_name = 'reporting/machinevm/add_machine.html'
    context_object_name = "vm"
    success_url = reverse_lazy("inventaires")


@method_decorator(role_required("Admin RHS"), name='dispatch')
class MachineUpdateView(UpdateView):
    model = MachineVM
    form_class = MachineForm
    template_name = 'reporting/machinevm/update_vm.html'
    context_object_name = "vm"
    success_url = reverse_lazy("inventaires")


@method_decorator(role_required("Admin RHS"), name='dispatch')
class MachineDetailView(DetailView):
    model = MachineVM
    template_name = 'reporting/machinevm/machine_vm_details_view.html'
    context_object_name = "vm"


@method_decorator(role_required("Admin RHS"), name='dispatch')
class MachineDeleteView(DeleteView):
    model = MachineVM
    template_name = 'reporting/machinevm/delete_vm.html'
    context_object_name = "vm"
    success_url = reverse_lazy("inventaires")


@method_decorator(login_required, name="dispatch")
class MachineVMViewSet(ReadOnlyModelViewSet):
    serializer_class = MachineVMSerializer

    def get_queryset(self):
        queryset = MachineVM.objects.all()
        year = self.request.GET.get('year')
        month = self.request.GET.get('month')
        if month is not None and year is not None:
            queryset = queryset.filter(import_month=month, import_year=year)
        return queryset


class ConfigVersionHSViewSet(ReadOnlyModelViewSet):
    serializer_class = ConfigVersionHSSerializer

    def get_queryset(self):
        queryset = ConfigVersionHS.objects.all()
        return queryset


class UserLoginView(LoginView):
    template_name = "registration/login.html"
    form_class = LoginForm


class UserLogoutView(LogoutView):
    template_name = "logout_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_year'] = month_year()[1]
        return context


class MyDetailView(TemplateView):
    template_name = 'reporting/reportpdf/report_pdf_temp.html'


@method_decorator(role_required("Admin RHS"), name='dispatch')
class ConfigView(ListView):
    model = ConfigVersionHS
    template_name = 'reporting/config/config.html'
    context_object_name = 'configs'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        role = self.request.user.role
        # context["role"] = role
        # context['list_role'] = ["Admin RHS", "Manager"]
        context['is_in_list_permitted_rhs'] = role in ["Admin RHS", "Manager"]
        context["is_admin_rhs"] = role == "Admin RHS"
        return context


@method_decorator(role_required("Admin RHS"), name='dispatch')
class CreateConfigView(CreateView):
    model = ConfigVersionHS
    template_name = 'reporting/config/add_config.html'
    context_object_name = 'configs'
    form_class = ConfigForm
    success_url = reverse_lazy("config")


@method_decorator(role_required("Admin RHS"), name='dispatch')
class DeleteConfigView(DeleteView):
    model = ConfigVersionHS
    template_name = 'reporting/config/delete_config.html'
    context_object_name = 'configs'
    success_url = reverse_lazy("config")


@login_required()
def view_pdf(request):
    day = datetime.today().strftime('%d')
    month = datetime.today().strftime('%m')
    year = datetime.today().strftime('%Y')
    buffer = create_pdf_buffer(request.user.first_name, request.user.last_name)
    return FileResponse(buffer, as_attachment=True, filename=f"rapport-{year}-{month}-{day}.pdf")
