from django.urls import path
from .views import index, InventaireView, Dashboard, MachineVMAPIView, MachineVMViewset, ImportCSV
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
                  path('index/', index, name='index'),
                  path('dashboard/', Dashboard.as_view(), name='dashboard'),
                  path('inventaires/', InventaireView.as_view(), name='inventaires'),
                  path('importfile/', ImportCSV.as_view(), name="importer"),
                  # path('api/machines/',MachineVMAPIView.as_view(), name='apimachines'),
                  # path('edit/<str:slug>/', MachineUpdate.as_view(), name='modifier')

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
