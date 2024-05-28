import io

from django.core.mail import send_mail, EmailMessage
from reportingauto.settings import EMAIL_HOST_USER

from .utils_pdf import create_pdf_buffer


def send_monthly_email():
    pdf_buffer = create_pdf_buffer("report", "admin")
    email = EmailMessage(
        "Rapport Mensuel",
        "Le rapport Mensuel du mois Mai",
        EMAIL_HOST_USER,
        ['abdelbassitalamine@gmail.com'],  # Liste des destinataires
    )
    email.attach('document.pdf', pdf_buffer.getvalue(), 'application/pdf')
    email.send()
