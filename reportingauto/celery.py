from __future__ import absolute_import, unicode_literals
import os
from celery import Celery


# Définir les variables d'environnement pour le module de réglages de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reportingauto.settings')

# Créer une instance de Celery
app = Celery('reportingauto')

# Charger la configuration de Celery depuis les réglages de Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks dans les applications installées (basé sur les décorateurs @shared_task)
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
