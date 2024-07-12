from __future__ import absolute_import, unicode_literals


from celery import shared_task
from reporting.email import send_monthly_email
from celery.utils.log import get_task_logger
from .csv_file_processing import download_csv, import_csv

logger = get_task_logger(__name__)



@shared_task
def send_monthly_email_task():
    logger.info('Sending monthly email')
    return send_monthly_email("Rapport Mensuel", "Veuillez recevoir le rapport")


@shared_task
def update_path_task():
    pass

