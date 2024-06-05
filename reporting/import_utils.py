import csv
from datetime import datetime


def add_date_fields_to_csv(input_file_path, output_file_path):
    # Obtenez le mois et l'année actuels
    current_date = datetime.now()
    import_month = current_date.strftime('%m')
    import_year = current_date.strftime('%Y')

    # Lisez le fichier CSV d'origine
    with open(input_file_path, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        fieldnames = reader.fieldnames + ['import_month', 'import_year']

        # Écrivez le nouveau fichier CSV avec les champs supplémentaires
        with open(output_file_path, 'w', newline='') as csvfile_out:
            writer = csv.DictWriter(csvfile_out, fieldnames=fieldnames)
            writer.writeheader()
            for row in reader:
                row['import_month'] = import_month
                row['import_year'] = import_year
                writer.writerow(row)