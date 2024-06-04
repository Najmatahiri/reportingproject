import io

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
from .forms import MachineForm, UploadFileForm, UserAdminRegistrationForm, LoginForm, ConfigForm
from reporting.serializers import MachineVMSerializer, ConfigVersionHSSerializer
from tablib import Dataset
from .ressources import MachineVMResource
from .decorators import access_required, role_required
from reportingauto.settings import EMAIL_HOST_USER
from django.http import FileResponse
from .utils_pdf import create_pdf_buffer
from .utils import get_lit_out_of_support, get_list_in_support, month_year


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


# def handler404(request, exception):
#     return render(request, '404.html', status=404)
#
#
# def handler500(request):
#     return render(request, '500.html', status=500)


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
        try:
            fichier_csv = form.cleaned_data['csv_file']
            chunk_size = 500
            for chunk in pd.read_csv(fichier_csv, chunksize=chunk_size):
                dataset = Dataset().load(chunk)
                machinevm_resource = MachineVMResource()
                result = machinevm_resource.import_data(dataset, dry_run=True, raise_errors=True)
                if not result.has_errors():
                    machinevm_resource.import_data(dataset, dry_run=False)
                else:
                    raise Exception("Erreur lors de l'importation")
            print("Fichier importé avec succès")
            return super().form_valid(form)
        except Exception as e:
            return self.render_to_response(self.get_context_data(form=form, error=str(e)))

    # def form_valid(self, form):
    #     try:
    #         fichier_csv = form.cleaned_data['csv_file']
    #         df = pd.read_csv(fichier_csv)
    #         print(df)
    #         dataset = Dataset().load(df)
    #         print(dataset)
    #         machinevm_resource = MachineVMResource()
    #         result = machinevm_resource.import_data(dataset, dry_run=True, raise_errors=True)
    #         if not result.has_errors():
    #             result = machinevm_resource.import_data(dataset, dry_run=False)
    #             print(result)
    #             print("fichier importer")
    #             return super().form_valid(form)
    #             # return HttpResponseRedirect(self.get_success_url(), status=302)
    #         else:
    #             print("Erreur lors de l'importation")
    #             raise Exception("Erreur lors de l'importation")
    #     except Exception as e:
    #         return self.render_to_response(self.get_context_data(form=form, error=str(e)))
    #


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
            date_import__month=month_year()[0],
            date_import__year=month_year()[1]
        ).count()

        role = self.request.user.role
        context["role"] = role
        context['is_in_list_permitted_rhs'] = role in ["Admin RHS", "Manager"]
        context["is_admin_rhs"] = role == "Admin RHS"
        context['inventaires'] = get_list_in_support()
        return context


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
            queryset = queryset.filter(date_import__month=month, date_import__year=year)
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
        return  context


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
    buffer = create_pdf_buffer(request.user.first_name, request.user.last_name)
    return FileResponse(buffer, as_attachment=False, filename="report.pdf")
