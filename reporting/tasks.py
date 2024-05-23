import io

from django.core.mail import send_mail, EmailMessage
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

from .models import MachineVM
from .utils_pdf import create_data_tab, additionner_tableaux, create_sum_criticality_tab
from .utils import month_year
from .views import data_out_of_support_machines, data


def create_pdf_buffer():
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
        " report admin",
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

    return buffer


def send_monthly_email():
    pdf_buffer = create_pdf_buffer()
    email = EmailMessage(
        "Rapport Mensuel",
        "Le rapport Mensuel du mois Mai",
        EMAIL_HOST_USER,
        ['abdelbassitalamine@gmail.com'],  # Liste des destinataires
    )
    # send_mail(
    #     'Rapport mensuel',
    #     'Veuillez recevoir ci-joint le rapport mensuel',
    #     EMAIL_HOST_USER,
    #     ['abdelbassitalamine@gmail.com'],
    #     fail_silently=False,
    # )

    email.attach('document.pdf', pdf_buffer.getvalue(), 'application/pdf')
    email.send()

