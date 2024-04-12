import pandas as pd
from django.urls import reverse_lazy
from django.core.mail import send_mail
from datetime import datetime
from django.db.models import Sum
from django.utils.decorators import method_decorator
from django.views.generic import ListView, UpdateView, DetailView, DeleteView, FormView
from django.views import View
from django.contrib.auth.views import LoginView, LogoutView

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from django.contrib.auth.decorators import login_required
from reporting.models import MachineVM
from .forms import MachineForm, UploadFileForm, UserAdminRegistrationForm
from reporting.serializers import MachineVMSerializer
from tablib import Dataset
from .ressources import MachineVMResource
from .decorators import access_required
from reportingauto.settings import EMAIL_HOST_USER

from .utils import render_to_pdf


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


def send_welcome_email(request):
    subject = 'Welcome to My Site'
    message = 'Thank you for creating an account!'
    from_email = EMAIL_HOST_USER
    recipient_list = ['abdelbassitalamine@gmail.com']
    send_mail(subject, message, from_email, recipient_list)
    return HttpResponse("<h1>Le message a été bien envoyé</h1>")


# Importer un fichier csv
@method_decorator(access_required, name='dispatch')
@method_decorator(login_required, name="dispatch")
class ImportCSV(FormView):
    template_name = 'reporting/utils/import_csv.html'
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
            print("fichier importer")
            return HttpResponseRedirect(self.get_success_url())

        return HttpResponse("<h1> Erreur lors de l'importation</h1>")


@method_decorator(access_required, name='dispatch')
@method_decorator(login_required, name="dispatch")
class Dashboard(ListView):
    model = MachineVM
    template_name = 'reporting/dashboard/dashboard.html'
    context_object_name = 'inventaires'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        date = datetime.today()
        somme_patchs = MachineVM.objects.aggregate(
            total_critical=Sum("critical"),
            total_important=Sum("important"),
            total_moderate=Sum("moderate"),
            total_low=Sum("low"),
        )
        context["date_now"] = date
        context['somme_patchs'] = somme_patchs
        return context


@method_decorator(login_required, name="dispatch")
class InventaireView(ListView):
    model = MachineVM
    template_name = 'reporting/inventaires/inventaires.html'
    context_object_name = 'inventaires'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["nb_patched"] = MachineVM.objects.filter(critical__gt=0).count()
        context["total_machine"] = MachineVM.objects.all().count()
        return context


@method_decorator(access_required, name='dispatch')
@method_decorator(login_required, name="dispatch")
class MachineUpdateView(UpdateView):
    model = MachineVM
    form_class = MachineForm
    template_name = 'reporting/machinevm/update_vm.html'
    context_object_name = "vm"
    success_url = reverse_lazy("inventaires")


@method_decorator(access_required, name='dispatch')
@method_decorator(login_required, name="dispatch")
class MachineDetailView(DetailView):
    model = MachineVM
    template_name = 'reporting/machinevm/machine_vm_details_view.html'
    context_object_name = "vm"


@method_decorator(access_required, name='dispatch')
@method_decorator(login_required, name="dispatch")
class MachineDeleteView(DeleteView):
    model = MachineVM
    template_name = 'reporting/machinevm/delete_vm.html'
    context_object_name = "vm"
    success_url = reverse_lazy("inventaires")


@method_decorator(access_required, name='dispatch')
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


class UserLoginView(LoginView):
    template_name = "registration/login.html"


class UserLogoutView(LogoutView):
    pass


class ViewPDF(View):
    def get(self, request, *args, **kwargs):
        pdf = render_to_pdf('reporting/reportpdf/report_template.html')
        return HttpResponse(pdf, content_type='application/pdf')


class DownloadPDF(View):
    def get(self, request, *args, **kwargs):
        pdf = render_to_pdf('reporting/reportpdf/report_template.html')

        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Rapport_%s.pdf" % ("Mensuel")
        content = "attachment; filename='%s'" % (filename)
        response['Content-Disposition'] = content
        return response


