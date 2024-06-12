import io
from reportlab.graphics.charts.doughnut import Doughnut
from reportlab.graphics.charts.piecharts import Pie
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from django.db.models import Sum
from .pdf_lab import create_header, create_header_details_paragraph, create_section_title, create_table, \
    create_bar_chart, create_footer, create_table_for_more_info, pie_chart_with_legend
from reporting.utils import month_year, get_lit_out_of_support, get_stat_out_of_support, get_details_patch_os, \
    get_list_in_support


def create_data_tab(group):
    """
    Crée un tableau contenant le nombre de machines patchées et non patchées pour un groupe donné.

    Args:
        group (str): Le groupe pour lequel les données sont récupérées.

    Returns:
        list: Un tableau contenant le nombre de machines patchées et non patchées.

    Raises:
        ValueError: Si le groupe spécifié est vide ou invalide.
    """
    if not group:
        raise ValueError("Le groupe ne peut pas être vide")

    vm_supported = get_list_in_support()
    try:
        nb_patched = vm_supported.filter(group=group, critical__exact=0).count()
        nb_not_patched = vm_supported.filter(group=group, critical__gt=0).count()
    except Exception as e:
        raise RuntimeError("Une erreur s'est produite lors de la récupération des données") from e

    return [nb_patched, nb_not_patched]


def _sum_criticality_level(criticality_level):
    """
    Calcule la somme des niveaux de criticité pour un niveau donné.

    Args:
        criticality_level (str): Le niveau de criticité pour lequel la somme est calculée.

    Returns:
        dict: Un dictionnaire contenant le résultat de la somme pour le niveau de criticité spécifié.

    Raises:
        RuntimeError: Si une erreur se produit lors de la récupération des données.
    """
    vm_supported = get_list_in_support()
    try:
        return vm_supported.aggregate(Sum(criticality_level))
    except Exception as e:
        raise RuntimeError("Une erreur s'est produite lors du calcul de la somme de criticité") from e


def create_sum_criticality_tab():
    """
    Crée un tableau contenant la somme des niveaux de criticité pour chaque niveau de criticité.

    Returns:
        list: Un tableau contenant la somme des niveaux de criticité pour chaque niveau.

    Raises:
        RuntimeError: Si une erreur se produit lors du calcul de la somme de criticité.
    """
    try:
        sum_critical = _sum_criticality_level('critical')
        sum_important = _sum_criticality_level('important')
        sum_moderate = _sum_criticality_level('moderate')
        sum_low = _sum_criticality_level('low')
    except RuntimeError as e:
        raise e

    tab = [
        ["Critical", sum_critical.get('critical__sum', 0)],
        ["Important", sum_important.get('important__sum', 0)],
        ["Moderate", sum_moderate.get('moderate__sum', 0)],
        ["Low", sum_low.get('low__sum', 0)],
    ]
    return tab


def additionner_tableaux(tab1, tab2):
    """
    Additionne deux tableaux élément par élément.

    Args:
        tab1 (list): Le premier tableau.
        tab2 (list): Le deuxième tableau.

    Returns:
        list: Le résultat de l'addition des deux tableaux.

    Raises:
        ValueError: Si les tableaux n'ont pas la même taille.
    """
    if len(tab1) != len(tab2):
        raise ValueError("Les tableaux doivent avoir la même taille")
    result = []
    try:
        for i in range(len(tab1)):
            result.append(tab1[i] + tab2[i])
    except Exception as e:
        raise RuntimeError("Une erreur s'est produite lors de l'addition des tableaux") from e
    return result


def create_pdf_buffer(user_firstname, user_lastname):
    """
    Crée un rapport PDF contenant diverses statistiques sur les machines, la criticité des vulnérabilités et l'état des patchs.

    Args:
        user_firstname (str): Le prénom de l'utilisateur qui génère le rapport.
        user_lastname (str): Le nom de l'utilisateur qui génère le rapport.

    Returns:
        io.BytesIO: Un tampon contenant le rapport PDF.

    Raises:
        RuntimeError: Si une erreur se produit lors de la génération du PDF.
    """
    try:
        # Collecte des données
        data_tab_prod = create_data_tab("PROD")
        data_tab_hors_prod = create_data_tab("Hors-Prod")
        data_tab_total = additionner_tableaux(data_tab_prod, data_tab_hors_prod)
        data_tab_criticality = create_sum_criticality_tab()[:2]
        data_tab_stat_path = [
            ["PROD", data_tab_prod[0], data_tab_prod[1]],
            ["HORS PROD", data_tab_hors_prod[0], data_tab_hors_prod[1]],
            ["Total", data_tab_total[0], data_tab_total[1]],

        ]

        data_tab_stat_path_total = [
            ["PROD", data_tab_prod[0], data_tab_prod[1], data_tab_prod[0] + data_tab_prod[1]],
            ["HORS PROD", data_tab_hors_prod[0], data_tab_hors_prod[1], data_tab_hors_prod[0] + data_tab_hors_prod[1]],
            ["Total", data_tab_total[0], data_tab_total[1], data_tab_total[0] + data_tab_total[1]]

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

        # Création du PDF
        buffer = io.BytesIO()
        canv = canvas.Canvas(buffer, pagesize=A4)
        styles = getSampleStyleSheet()

        # En-tête
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

        # Section 1 : Statistiques de la criticité et des patchs
        create_section_title(
            "Statistique de la Criticité  des Vulnérabilités et de l'État des Patches des Machines",
            styles, canv, 10, 650
        )
        table_data_criticality = [["Sévérité", "Nombre"]] + data_tab_criticality
        create_table(table_data_criticality, canv, 50, 562)
        table_data_production = [["", "PATCHED", "NOT PATCHED", "SUM"]] + data_tab_stat_path_total
        create_table(table_data_production, canv, 250, 545)

        # Section 2 : Visualisation graphique des statistiques de patchs
        create_section_title(
            "Visualisation Graphique des statistiques de Patchs des Machines",
            styles, canv, 10, 480
        )
        d = pie_chart_with_legend(data_tab_prod, "PROD", Doughnut(), True)
        d.drawOn(canv, -52, 280)
        d1 = pie_chart_with_legend(data_tab_hors_prod, "HORS PROD", Doughnut())
        d1.drawOn(canv, 60, 285)
        d2 = pie_chart_with_legend(data_tab_total, "TOTAL", Pie())
        d2.drawOn(canv, 252, 280)

        # Section 3 : Graphique des détails des patchs
        categorises = data_tab_patch_os['os_versions']
        data_patch_os = data_tab_patch_os['data']
        create_bar_chart(data_patch_os, categorises, canv, 100, 100)

        # Pied de page 1
        create_footer(canv, 1)
        canv.showPage()

        create_header(canv)

        # Section 4 : Top 20 des Machines critiques
        create_section_title(
            "Top 20 des Machines critiques",
            styles, canv, 10, 750
        )
        table_data_top_critical = [["Nom", "IP", "Groupe", "OS", "Critical"]] + data_tab_top_machine
        create_table(table_data_top_critical, canv, 100, 350)

        # Pied de page 2
        create_footer(canv, 2)
        canv.showPage()

        create_header(canv)

        # Section 5 : Liste des machines hors support
        create_section_title(
            "List des machines Hors support",
            styles, canv, 10, 730
        )
        table_data_out_of_support = [["Nom", "IP", "Groupe", "OS"]] + data_tab_hs
        create_table(table_data_out_of_support, canv, 10, 240)
        create_table_for_more_info(data_tab_stat_hs, canv, 450, 630)

        # Pied de page 3
        create_footer(canv, 3)
        # Enregistrement du fichier PDF
        canv.save()
        buffer.seek(0)
        return buffer

    except Exception as e:
        print(e)
        buffer = io.BytesIO()
        canv = canvas.Canvas(buffer, pagesize=A4)

        styles = getSampleStyleSheet()
        canv.drawString(100, 100, "Pas de donnée à afficher")
        canv.save()
        buffer.seek(0)
        return buffer
