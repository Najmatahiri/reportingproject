from datetime import datetime

from reporting.models import ConfigVersionHS, MachineVM


def month_year(date=datetime.today().strftime('%d-%m-%Y')):
    current_date__month = date.split('-')[1]
    current_date__year = date.split('-')[2].lstrip('0')
    return current_date__month, current_date__year


def get_redhat_major_versions():
    current_month = month_year()[0]
    current_year = month_year()[1]
    unsupported_versions = ConfigVersionHS.objects.values_list('unsupported_versions', flat=True)

    # Récupérer toutes les machines dont le système d'exploitation est RedHat
    machines = MachineVM.objects.filter(
        date_import__month=current_month,
        date_import__year=current_year)

    # Récupérer les versions de RedHat hors service (EOL)

    redhat_versions = set()

    for machine in machines:

        os_version = machine.os
        # Extraire la version majeure de RedHat (par exemple, 8 de "RedHat 8.7")
        if "RedHat" in os_version:
            version_major = os_version.split()[1].split('.')[0]
            redhat_versions.add(f'RedHat {version_major}')

    for version in unsupported_versions:
        if version in redhat_versions:
            redhat_versions.remove(version)

    return sorted(redhat_versions)


def get_lit_out_of_support():
    list_hs = ConfigVersionHS.objects.all()
    # tab_hs = [version.unsupported_versions for version in list_hs]
    machine_hs_filtre = []
    for version in list_hs:
        machine_hs = MachineVM.objects.filter(
            os__startswith=f"{version}.",
            date_import__month=month_year()[0],
            date_import__year=month_year()[1]
        )
        machine_hs_filtre.extend(machine_hs)

    return machine_hs_filtre


def get_stat_out_of_support():
    list_hs = ConfigVersionHS.objects.all()
    tab_hs = [version.unsupported_versions for version in list_hs]
    stat_hs_tab = []
    total_hs = 0

    current_month, current_year = month_year()

    for version in tab_hs:
        machine_hs = MachineVM.objects.filter(os__startswith=f"{version}.",
                                              date_import__month=current_month,
                                              date_import__year=current_year)
        stat_hs = [(version, len(machine_hs))]
        total_hs += len(machine_hs)
        stat_hs_tab.extend(stat_hs)
    stat_hs_tab.extend([("Total", total_hs)])
    return stat_hs_tab


def get_details_patch_os():
    version_os = get_redhat_major_versions()
    stat_patchs_os = {}
    data_tab_stat_os = []
    for version in version_os:
        nb_patched = MachineVM.objects.filter(
            os__startswith=f"{version}.",
            critical__exact=0,
            date_import__month=month_year()[0],
            date_import__year=month_year()[1]
        ).count()
        nb_not_patched = MachineVM.objects.filter(
            os__startswith=f"{version}.",
            critical__gt=0,
            date_import__month=month_year()[0],
            date_import__year=month_year()[1]
        ).count()

        stat_version_os = [(nb_patched, nb_not_patched)]
        data_tab_stat_os.extend(stat_version_os)

    reorganized_data = list(zip(*data_tab_stat_os))

    data_os = [tuple(reorganized_data[0]), tuple(reorganized_data[1])]

    stat_patchs_os["os_versions"] = version_os
    stat_patchs_os["data"] = data_os

    return stat_patchs_os


def get_list_in_support(order_field="nom_machine"):
    version_supported = get_redhat_major_versions()
    month, year = month_year()

    # Create an empty QuerySet for chaining
    machines_supported = MachineVM.objects.none()

    for version in version_supported:
        machines_supported = machines_supported | MachineVM.objects.filter(
            os__startswith=f"{version}.",
            date_import__month=month,
            date_import__year=year
        )
    # Order by the specified field
    machines_supported = machines_supported.order_by(f"-{order_field}")

    return machines_supported
