import pandas as pd
from django.urls import reverse_lazy
from django.core.mail import send_mail
from datetime import datetime
from django.db.models import Sum
from django.utils.decorators import method_decorator
from django.views.generic import ListView, UpdateView, DetailView, DeleteView, FormView, TemplateView
from django.views import View
from django.contrib.auth.views import LoginView, LogoutView

from django.conf import settings

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

from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfgen import canvas

from django.templatetags.static import static

from django.http import FileResponse
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Image, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

import io

from reporting.pdf_lab import pie_chart_with_legend, create_table, data_table

from datetime import datetime

from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.doughnut import Doughnut

APP_ROOT = "reporting"


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


# @method_decorator(access_required, name='dispatch')
# @method_decorator(login_required, name="dispatch")
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


class MyDetailView(TemplateView):
    # vanilla Django DetailView
    template_name = 'reporting/reportpdf/report_pdf_temp.html'


def view_pdf(request):
    nb_prod_patched = MachineVM.objects.filter(group="PROD", critical__exact=0).count()
    nb_prod_not_patched = MachineVM.objects.filter(group="PROD", critical__gt=0).count()
    nb_hors_prod_patched = MachineVM.objects.filter(group="HORS-PROD", critical__exact=0).count()
    nb_hors_prod_not_patched = MachineVM.objects.filter(group="HORS-PROD", critical__gt=0).count()
    nb_total_patched = nb_prod_patched + nb_hors_prod_patched
    nb_total_no_patched = nb_prod_not_patched + nb_hors_prod_not_patched

    datab_prod = [nb_prod_patched, nb_prod_not_patched]
    datab_hors_prod = [nb_hors_prod_patched, nb_hors_prod_not_patched]
    datab_total = [nb_total_patched, nb_total_no_patched]

    datable_prod = data_table(nb_prod_patched, nb_prod_not_patched, "PROD")
    datable_hors_prod = data_table(nb_hors_prod_patched, nb_hors_prod_not_patched, "HORS PROD")
    datable_total = data_table(nb_total_patched, nb_total_no_patched, "TOTAL")

    image_path = APP_ROOT + static("images/absLogo-3.jpg")

    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    styles = getSampleStyleSheet()
    canv = canvas.Canvas(buffer, pagesize=A4)

    logo = Image(image_path, width=100, height=100)
    logo.hAlign = "LEFT"
    logo.drawOn(canv, 10, 750)

    date_style = ParagraphStyle(name='default', fontSize=12, leading=24)
    current_date = datetime.today().strftime('%Y-%m-%d')
    date = Paragraph(current_date, date_style)
    date.wrap(300, 500)
    date.drawOn(canv, 400, 790)
    canv.line(10, 780, 580, 780)

    title_style = styles['Title']
    title = Paragraph("Rapport Mensuel", title_style)
    title.hAlign = "CENTER"
    title.wrap(400, 300)
    title.drawOn(canv, 100, 700)

    d = pie_chart_with_legend(datab_prod, "PROD", Doughnut())
    d1 = pie_chart_with_legend(datab_hors_prod, "HORS PROD", Doughnut())
    d2 = pie_chart_with_legend(datab_total, "TOTAL", Pie())
    table_prod = create_table(datable_prod)
    table_hors_prod = create_table(datable_hors_prod)
    table_total = create_table(datable_total)
    table_prod.wrap(200, 200)
    table_hors_prod.wrap(200, 200)
    table_total.wrap(200, 200)

    # les graphes et Tableaux

    # PROD
    d.drawOn(canv, 10, 500)
    table_prod.drawOn(canv, 400, 570)
    #hors prod
    d1.drawOn(canv, 10, 330)
    table_hors_prod.drawOn(canv, 400, 390)

    #total
    d2.drawOn(canv, 10, 160)
    table_total.drawOn(canv, 400, 220)

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    canv.showPage()
    canv.save()

    buffer.seek(0)
    return FileResponse(buffer, as_attachment=False, filename="report.pdf")
