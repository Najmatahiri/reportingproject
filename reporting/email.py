from django.core.mail import EmailMessage
from reportingauto.settings import EMAIL_HOST_USER
from .utils_pdf import create_pdf_buffer
from datetime import datetime


def send_monthly_email(objet, contenu):
    pdf_buffer = create_pdf_buffer("report", "admin")
    day = datetime.today().strftime('%d')
    month = datetime.today().strftime('%m')
    year = datetime.today().strftime('%Y')
    email = EmailMessage(
        objet,
        contenu,
        EMAIL_HOST_USER,
        ['abdelbassitalamine@gmail.com'],
    )
    email.attach(f"rapport-{year}-{month}-{day}.pdf", pdf_buffer.getvalue(), 'application/pdf')
    return email.send(fail_silently=False)
