from django.urls import path, include
from .views import index, InventaireView, Dashboard, ImportCSV, MachineDetailView, MachineUpdateView, MachineDeleteView, signup
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('index/', index, name='index'),
                  path('dashboard/', Dashboard.as_view(), name='dashboard'),
                  path('inventaires/', InventaireView.as_view(), name='inventaires'),
                  path('importfile/', ImportCSV.as_view(), name="importer"),
                  path('inventaires/edit/<str:slug>/', MachineUpdateView.as_view(), name='update-vm'),
                  path('inventaires/delete/<str:slug>/', MachineDeleteView.as_view(), name='delete-vm'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
