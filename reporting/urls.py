from django.urls import path, include

import reporting
from .views import index, InventaireView, Dashboard, ImportCSV, MachineDetailView, MachineUpdateView, MachineDeleteView, \
    signup, send_welcome_email, view_pdf, ConfigView,  CreateConfigView, DeleteConfigView
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth.views import LogoutView

urlpatterns = [
                  path('index/', index, name='index'),
                  path('dashboard/', Dashboard.as_view(), name='dashboard'),
                  path('send-welcome-email/', send_welcome_email, name='send_welcome_email'),
                  path('inventaires/', InventaireView.as_view(), name='inventaires'),
                  path('importfile/', ImportCSV.as_view(), name="importer"),
                  path('inventaires/edit/<str:slug>/', MachineUpdateView.as_view(), name='update-vm'),
                  path('inventaires/delete/<str:slug>/', MachineDeleteView.as_view(), name='delete-vm'),
                  path('config/', ConfigView.as_view(), name="config"),
                  path("view_pdf/", view_pdf, name="view_pdf"),
                  path('add-config-version-hs/', CreateConfigView.as_view(), name='add-config'),
                  path('config/delete/<str:slug>/', DeleteConfigView.as_view(), name='delete-config-hs'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


