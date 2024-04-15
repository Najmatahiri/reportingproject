from django.urls import path, include
from .views import index, InventaireView, Dashboard, ImportCSV, MachineDetailView, MachineUpdateView, MachineDeleteView, \
    signup, send_welcome_email, ViewPDF, DownloadPDF, PrintView, view_pdf
from django.conf import settings
from django.conf.urls.static import static
import reporting.plotly_dash

urlpatterns = [
                  path('index/', index, name='index'),
                  path('dashboard/', Dashboard.as_view(), name='dashboard'),
                  path('send-welcome-email/', send_welcome_email, name='send_welcome_email'),
                  path('inventaires/', InventaireView.as_view(), name='inventaires'),
                  path('importfile/', ImportCSV.as_view(), name="importer"),
                  path('inventaires/edit/<str:slug>/', MachineUpdateView.as_view(), name='update-vm'),
                  path('inventaires/delete/<str:slug>/', MachineDeleteView.as_view(), name='delete-vm'),
                  path('pdf_view/', ViewPDF.as_view(), name="pdf_view"),
                  path('pdf_download/', DownloadPDF.as_view(), name="pdf_download"),
                  path('print_view/', PrintView.as_view(), name="print_view"),
                  path("view_pdf/", view_pdf, name="view_pdf"),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
