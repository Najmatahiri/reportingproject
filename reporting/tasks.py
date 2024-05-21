from django.core.mail import send_mail
from reportingauto.settings import EMAIL_HOST_USER


def send_monthly_email():
    send_mail(
        'Rapport mensuel',
        'Veuillez recevoir ci-joint le rapport mensuel',
        EMAIL_HOST_USER,
        ['abdelbassitalamine@gmail.com'],
        fail_silently=False,
    )
