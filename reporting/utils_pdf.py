from .models import MachineVM
from django.db.models import Sum
from .utils import month_year


def create_data_tab(group):
    nb_patched = MachineVM.objects.filter(group=group, critical__exact=0,
                                          date_import__month=month_year()[0],
                                          date_import__year=month_year()[1]).count()
    nb_not_patched = MachineVM.objects.filter(group=group, critical__gt=0,
                                              date_import__month=month_year()[0],
                                              date_import__year=month_year()[1]
                                              ).count()
    return [nb_patched, nb_not_patched]


def _sum_criticality_level(criticality_level):
    return (MachineVM.objects.filter(
        date_import__month=month_year()[0],
        date_import__year=month_year()[1]
             ).aggregate(Sum(criticality_level)))


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
