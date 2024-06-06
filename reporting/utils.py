from datetime import datetime
from reporting.models import ConfigVersionHS, MachineVM


def month_year(date=datetime.today().strftime('%d-%m-%Y')):
    """
    Returns the current month and year from a given date string.

    Parameters:
    date (str): Date string in the format 'dd-mm-yyyy'. Defaults to today's date.

    Returns:
    tuple: A tuple containing the month and the year as strings.
    """
    try:
        current_date__month = date.split('-')[1]
        current_date__year = date.split('-')[2].lstrip('0')
        print(type(current_date__year))
        print(current_date__year)
        return current_date__month, current_date__year

    except Exception as e:
        print(f"Error in month_year: {e}")
        return None, None


def get_tab_num_hs():
    """
    Retrieves a list of unsupported version numbers from the ConfigVersionHS model.

    Returns:
    list: A list of integers representing unsupported version numbers.
    """
    try:
        list_hs = ConfigVersionHS.objects.all()
        tab_hs = [version.unsupported_versions for version in list_hs]
        tab = []
        for version in tab_hs:
            num = version.split()[1]
            tab.append(int(num))
        return tab
    except Exception as e:
        print(f"Error in get_tab_num_hs: {e}")
        return []


def get_redhat_major_versions():
    """
    Retrieves a list of RedHat major versions currently in use, excluding unsupported versions.

    Returns:
    list: A sorted list of RedHat major versions.
    """
    try:
        current_month, current_year = month_year()
        if not current_month or not current_year:
            raise ValueError("Invalid date values")

        unsupported_versions = ConfigVersionHS.objects.values_list('unsupported_versions', flat=True)
        machines = MachineVM.objects.filter(import_month=current_month, import_year=current_year)
        redhat_versions = set()

        for machine in machines:
            os_version = machine.os
            if "RedHat" in os_version:
                version_major = os_version.split()[1].split('.')[0]
                redhat_versions.add(f'RedHat {version_major}')

        for version in unsupported_versions:
            if version in redhat_versions:
                redhat_versions.remove(version)

        return sorted(redhat_versions)
    except Exception as e:
        print(f"Error in get_redhat_major_versions: {e}")
        return []


def get_lit_out_of_support():
    """
    Retrieves a list of machines that are out of support based on their OS versions.

    Returns:
    list: A list of MachineVM objects that are out of support.
    """
    try:
        list_hs = ConfigVersionHS.objects.all()
        machine_hs_filtre = []
        for version in list_hs:
            machine_hs = MachineVM.objects.filter(
                os__startswith=f"{version}.",
                import_month=month_year()[0],
                import_year=month_year()[1]
            )
            machine_hs_filtre.extend(machine_hs)

        return machine_hs_filtre
    except Exception as e:
        print(f"Error in get_lit_out_of_support: {e}")
        return []


def get_stat_out_of_support():
    """
    Retrieves statistics of out-of-support machines based on their OS versions.

    Returns:
    list: A list of tuples containing the version and the number of out-of-support machines,
          along with a total count of all out-of-support machines.
    """
    try:
        list_hs = ConfigVersionHS.objects.all()
        tab_hs = [version.unsupported_versions for version in list_hs]
        stat_hs_tab = []
        total_hs = 0

        current_month, current_year = month_year()
        if not current_month or not current_year:
            raise ValueError("Invalid date values")

        for version in tab_hs:
            machine_hs = MachineVM.objects.filter(
                os__startswith=f"{version}.",
                import_month=current_month,
                import_year=current_year
            )
            stat_hs = [(version, len(machine_hs))]
            total_hs += len(machine_hs)
            stat_hs_tab.extend(stat_hs)
        stat_hs_tab.extend([("Total", total_hs)])
        return stat_hs_tab
    except Exception as e:
        print(f"Error in get_stat_out_of_support: {e}")
        return []


def get_details_patch_os():
    """
    Retrieves details about patched and unpatched machines for each RedHat major version.

    Returns:
    dict: A dictionary containing the RedHat major versions and corresponding patch statistics.
    """
    try:
        version_os = get_redhat_major_versions()
        stat_patchs_os = {}
        data_tab_stat_os = []
        for version in version_os:
            nb_patched = MachineVM.objects.filter(
                os__startswith=f"{version}.",
                critical__exact=0,
                import_month=month_year()[0],
                import_year=month_year()[1]
            ).count()
            nb_not_patched = MachineVM.objects.filter(
                os__startswith=f"{version}.",
                critical__gt=0,
                import_month=month_year()[0],
                import_year=month_year()[1]
            ).count()

            stat_version_os = [(nb_patched, nb_not_patched)]
            data_tab_stat_os.extend(stat_version_os)

        reorganized_data = list(zip(*data_tab_stat_os))

        data_os = [tuple(reorganized_data[0]), tuple(reorganized_data[1])]

        stat_patchs_os["os_versions"] = version_os
        stat_patchs_os["data"] = data_os

        return stat_patchs_os
    except Exception as e:
        print(f"Error in get_details_patch_os: {e}")
        return {}


def get_list_in_support(order_field="nom_machine"):
    """
    Retrieves a list of in-support machines based on their OS versions, ordered by a specified field.

    Parameters:
    order_field (str): The field to order the results by. Defaults to "nom_machine".

    Returns:
    QuerySet: A QuerySet of MachineVM objects that are in support, ordered by the specified field.
    """
    try:
        version_supported = get_redhat_major_versions()
        month, year = month_year()
        if not month or not year:
            raise ValueError("Invalid date values")

        machines_supported = MachineVM.objects.none()
        for version in version_supported:
            machines_supported = machines_supported | MachineVM.objects.filter(
                os__startswith=f"{version}.",
                import_month=month,
                import_year=year
            )

        machines_supported = machines_supported.order_by(f"-{order_field}")
        return machines_supported
    except Exception as e:
        print(f"Error in get_list_in_support: {e}")
        return MachineVM.objects.none()
