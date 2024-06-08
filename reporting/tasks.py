from __future__ import absolute_import, unicode_literals
from celery import shared_task
from reporting.email import send_monthly_email
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@shared_task
def add(x, y):
    print(x + y)
    return x + y


@shared_task
def send_monthly_email_task():
    logger.info('Sending monthly email')
    return send_monthly_email("Rapport Mensuel", "Veuillez recevoir le rapport")
