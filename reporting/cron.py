from django.core.mail import send_mail
from reportingauto.settings import EMAIL_HOST_USER
from django_cron import CronJobBase, Schedule


class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 1  # every 2 hours

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'reporting.my_cron_job'  # a unique code

    def do(self):
        # Envoyer un email à tous les utilisateurs
        send_mail(
            'Rapport mensuel',
            'Le rapport mensuel est disponible.',
            EMAIL_HOST_USER,
            ['abdelbassitalamine@gmail.com'],

        )
    # do your thing here  pass
