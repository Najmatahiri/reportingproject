import io
from reportlab.graphics.charts.doughnut import Doughnut
from reportlab.graphics.charts.piecharts import Pie
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from .models import MachineVM
from django.db.models import Sum
from .pdf_lab import create_header, create_header_details_paragraph, create_section_title, create_table, \
    create_bar_chart, create_footer, create_table_for_more_info, pie_chart_with_legend
from reporting.utils import month_year, get_lit_out_of_support, get_stat_out_of_support, get_details_patch_os, \
    get_list_in_support


def create_data_tab(group):
    vm_supported = get_list_in_support()
    nb_patched = vm_supported.filter(group=group, critical__exact=0).count()
    nb_not_patched = vm_supported.filter(group=group, critical__gt=0).count()
    return [nb_patched, nb_not_patched]


def _sum_criticality_level(criticality_level):
    vm_supported = get_list_in_support()
    return vm_supported.aggregate(Sum(criticality_level))


def create_sum_criticality_tab():
    sum_critical = _sum_criticality_level('critical')
    sum_important = _sum_criticality_level('important')
    sum_moderate = _sum_criticality_level('moderate')
    sum_low = _sum_criticality_level('low')

    tab = [
        ["Critical", sum_critical['critical__sum']],
        ["Important", sum_important['important__sum']],
        ["Moderate", sum_moderate['moderate__sum']],
        ["Low", sum_low['low__sum']],

    ]
    return tab


def additionner_tableaux(tab1, tab2):
    if len(tab1) != len(tab2):
        raise ValueError("Les tableaux doivent avoir la même taille")
    resultat = []
    for i in range(len(tab1)):
        resultat.append(tab1[i] + tab2[i])
    return resultat


def create_pdf_buffer(user_firstname, user_lastname):
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
    top_machines = get_list_in_support("critical")[:20]

    data_tab_top_machine = [
        (vm.nom_machine, vm.ip, vm.group, vm.os, vm.critical)
        for vm in top_machines
    ]

    machine_hs_filtre = get_lit_out_of_support()
    data_tab_hs = [(vm_hs.nom_machine, vm_hs.ip, vm_hs.group, vm_hs.os) for vm_hs in machine_hs_filtre]

    data_tab_stat_hs = get_stat_out_of_support()
    data_tab_patch_os = get_details_patch_os()

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
        f"{user_firstname}  {user_lastname}",
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
    categorises = data_tab_patch_os['os_versions']
    data_patch_os = data_tab_patch_os['data']
    create_bar_chart(data_patch_os, categorises, canv, 100, 100)
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
    table_data_out_of_support = [["Nom", "IP", "Groupe", "OS"]] + data_tab_hs
    create_table(table_data_out_of_support, canv, 10, 240)
    create_table_for_more_info(data_tab_stat_hs, canv, 450, 630)

    # Pied Page 3
    create_footer(canv, 3)
    # present the option to save the file.
    canv.save()
    buffer.seek(0)
    return buffer
