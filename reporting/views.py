import pandas as pd
import io
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
from reporting.serializers import MachineVMSerializer
from tablib import Dataset
from .ressources import MachineVMResource
from .decorators import access_required
from reportingauto.settings import EMAIL_HOST_USER
from reportlab.pdfgen import canvas
from django.http import FileResponse
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reporting.pdf_lab import pie_chart_with_legend, create_table, create_header, create_footer, create_bar_chart, \
    create_section_title, create_table_for_more_info, create_header_details_paragraph
from datetime import datetime
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.doughnut import Doughnut
from .utils_pdf import create_data_tab, additionner_tableaux, create_sum_criticality_tab
from .utils import month_year


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
        try:
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
                return HttpResponseRedirect(self.get_success_url(), status=302)
            else:
                raise Exception("Erreur lors de l'importation")
        except Exception as e:
            return self.render_to_response(self.get_context_data(form=form, error=str(e)))


@method_decorator(access_required, name='dispatch')
@method_decorator(login_required, name="dispatch")
class Dashboard(ListView):
    model = MachineVM
    template_name = 'reporting/dashboard/dashboard.html'
    context_object_name = 'inventaires'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        date = datetime.today().strftime('%Y-%m-%d')
        top_20 = MachineVM.objects.all().order_by('-critical')[:20]
        list_hs = ConfigVersionHS.objects.all()
        tab_hs = [version.unsupported_versions for version in list_hs]
        machine_hs_filtre = []
        for version in list_hs:
            machine_hs = MachineVM.objects.filter(os__startswith=f"{version}.")
            machine_hs_filtre.extend(machine_hs)

        total_hs = len(machine_hs_filtre)
        current_username = self.request.user.username
        context['username'] = current_username
        context['top_20'] = top_20
        context['machine_hs'] = machine_hs_filtre
        context['total_hs'] = total_hs
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
    form_class = LoginForm


class UserLogoutView(LogoutView):
    template_name = "registration/logged_out.html"


class MyDetailView(TemplateView):
    template_name = 'reporting/reportpdf/report_pdf_temp.html'


class ConfigView(ListView):
    model = ConfigVersionHS
    template_name = 'reporting/config/config.html'
    context_object_name = 'configs'


class AddConfigView(CreateView):
    model = ConfigVersionHS
    form_class = ConfigForm


# Data for the table
data = [
    ["Red Hat 5", 10],
    ["Red Hat 6", 20],
    ["Total", 30],
]

data_out_of_support_machines = [
    ("deltasig.localdomain", "10.4.1.191", "Hors-Prod", "RedHat 6.10"),
    ("deltasig.localdomain", "10.4.1.191", "Hors-Prod", "RedHat 6.10"),
    ("deltasig.localdomain", "10.4.1.191", "Hors-Prod", "RedHat 6.10"),
    ("deltasig.localdomain", "10.4.1.191", "Hors-Prod", "RedHat 6.10"),
    ("deltasig.localdomain", "10.4.1.191", "Hors-Prod", "RedHat 6.10"),
    ("deltasig.localdomain", "10.4.1.191", "Hors-Prod", "RedHat 6.10"),
    ("deltasig.localdomain", "10.4.1.191", "Hors-Prod", "RedHat 6.10"),
    ("deltasig.localdomain", "10.4.1.191", "PROD", "RedHat 5.10"),
    ("deltasig.localdomain", "10.4.1.191", "Hors-Prod", "RedHat 6.10"),
    ("deltasig.localdomain", "10.4.1.191", "Hors-Prod", "RedHat 6.10"),
    ("deltasig.localdomain", "10.4.1.191", "Hors-Prod", "RedHat 6.10"),
    ("deltasig.localdomain", "10.4.1.191", "Hors-Prod", "RedHat 6.10"),
    ("deltasig.localdomain", "10.4.1.191", "Hors-Prod", "RedHat 6.10"),
    ("deltasig.localdomain", "10.4.1.191", "Hors-Prod", "RedHat 6.10"),
    ("deltasig.localdomain", "10.4.1.191", "Hors-Prod", "RedHat 5.10"),
    ("deltasig.localdomain", "10.4.1.191", "Hors-Prod", "RedHat 6.10"),
    ("deltasig.localdomain", "10.4.1.191", "Hors-Prod", "RedHat 6.10"),
    ("deltasig.localdomain", "10.4.1.191", "Hors-Prod", "RedHat 6.10"),
    ("deltasig.localdomain", "10.4.1.191", "Hors-Prod", "RedHat 6.10"),
    ("deltasig.localdomain", "10.4.1.191", "Hors-Prod", "RedHat 6.10"),
    ("deltasig.localdomain", "10.4.1.191", "Hors-Prod", "RedHat 6.10"),
    ("deltasig.localdomain", "10.4.1.191", "Hors-Prod", "RedHat 6.10"),
    ("deltasig.localdomain", "10.4.1.191", "Hors-Prod", "RedHat 6.10"),
    ("deltasig.localdomain", "10.4.1.191", "Hors-Prod", "RedHat 6.10"),
    ("deltasig.localdomain", "10.4.1.191", "Hors-Prod", "RedHat 6.10"),

    # Add more rows as needed
]


def view_pdf(request):
    # les données
    data_tab_prod = create_data_tab("PROD")
    data_tab_hors_prod = create_data_tab("Hors-Prod")
    data_tab_total = additionner_tableaux(data_tab_prod, data_tab_hors_prod)
    data_tab_criticality = create_sum_criticality_tab()
    data_tab_stat_path = [
        ["PROD", data_tab_prod[0], data_tab_prod[1]],
        ["HORS PROD", data_tab_hors_prod[0], data_tab_hors_prod[1]],
        ["Total", data_tab_total[0], data_tab_total[1]],
    ]
    top_machines = MachineVM.objects.filter(
        date_import__month=month_year()[0],
        date_import__year=month_year()[1],
    ).order_by('-critical')[:20]

    data_tab_top_machine = [
        (vm.nom_machine, vm.ip, vm.group, vm.os, vm.critical)
        for vm in top_machines
    ]

    buffer = io.BytesIO()
    styles = getSampleStyleSheet()
    canv = canvas.Canvas(buffer, pagesize=A4)

    """
    ****************************************************************************************
     EN TETE
    ****************************************************************************************
    """
    create_header(canv)
    create_header_details_paragraph(
        "Equipe",
        "IAAS",
        styles, canv, 10, 740, 40
    )
    create_header_details_paragraph(
        "Généré par",
        f"{request.user.first_name}  {request.user.last_name}",
        styles, canv, 10, 720, 65
    )

    title_style = styles['Title']
    title = Paragraph("Rapport Mensuel", title_style)

    title.hAlign = "CENTER"
    title.wrap(400, 300)
    title.drawOn(canv, 100, 690)

    """
    ****************************************************************************************
    SECTION 1
    ****************************************************************************************
    """

    create_section_title(
        "Statistique de la Criticité  des Vulnérabilités et de l'État des Patches des Machines",
        styles, canv, 10, 650
    )

    table_data_criticality = [["Niveau", "Nombre"]] + data_tab_criticality
    create_table(table_data_criticality, canv, 50, 540)

    table_data_production = [["", "PATCHED", "NOT PATCHED"]] + data_tab_stat_path
    create_table(table_data_production, canv, 250, 545)

    """
    ****************************************************************************************
    SECTION 2
    ****************************************************************************************
     """
    create_section_title(
        "Visualisation Graphique des statistiques de Patchs des Machines",
        styles, canv, 10, 480
    )

    d = pie_chart_with_legend(data_tab_prod, "PROD", Doughnut(), True)
    d.drawOn(canv, -10, 280)
    d1 = pie_chart_with_legend(data_tab_hors_prod, "HORS PROD", Doughnut())
    d1.drawOn(canv, 110, 280)
    d2 = pie_chart_with_legend(data_tab_total, "TOTAL", Pie())
    d2.drawOn(canv, 270, 280)

    """
     ****************************************************************************************
     SECTION 3
     ****************************************************************************************
      """
    categorie_names = ['Red Hat 7', 'Red Hat 8', 'Red Hat 9']
    data_patch_os = [
        (10, 20, 30),  # Data series 1
        (15, 25, 10)  # Data series 2
    ]
    create_bar_chart(data_patch_os, categorie_names, canv, 100, 100)
    # drawing1.drawOn(canv, 100, 100)

    # Pied de page 1
    create_footer(canv, 1)
    canv.showPage()

    create_header(canv)

    """
      ****************************************************************************************
      SECTION 4
      ****************************************************************************************
    """

    create_section_title(
        "Top 20 des Machines critiques",
        styles, canv, 10, 750

    )

    table_data_top_critical = [["Nom", "IP", "Groupe", "OS", "Critical"]] + data_tab_top_machine
    create_table(table_data_top_critical, canv, 100, 350)

    # Pied Page 2
    create_footer(canv, 2)
    canv.showPage()

    create_header(canv)
    """
       ****************************************************************************************
       SECTION 5
       ****************************************************************************************
     """
    create_section_title(
        "List des machines  Hors support",
        styles, canv, 10, 730
    )
    table_data_out_of_support = [["Nom", "IP", "Groupe", "OS"]] + data_out_of_support_machines
    create_table(table_data_out_of_support, canv, 10, 240)

    create_table_for_more_info(data, canv, 450, 660)

    # Pied Page 3
    create_footer(canv, 3)

    # present the option to save the file.
    canv.save()

    buffer.seek(0)
    return FileResponse(buffer, as_attachment=False, filename="report.pdf")
