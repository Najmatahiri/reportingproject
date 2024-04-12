"""
URL configuration for reportingauto project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from reporting.views import MachineVMViewSet, signup, UserLoginView, UserLogoutView, index

from django.conf.urls.defaults import url, patterns
from wkhtmltopdf.views import PDFTemplateView


# Ici, nous créons notre routeur
router = routers.SimpleRouter()
# Puis lui déclarons une url basée sur le mot clé ‘category’ et notre view
# afin que l’url générée soit celle que nous souhaitons ‘/api/category/’
router.register('machines', MachineVMViewSet, basename='machines')


urlpatterns = [
    path('', index, name="index"),
    path('reporting/', include('reporting.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls)),
    path('accounts/signup/', signup, name='signup'),
    path('accounts/login/', UserLoginView.as_view(), name='login'),
    path('accounts/logout/', UserLoginView.as_view(), name='logout'),
    path('admin/', admin.site.urls),
    patterns('',
             url(r'^pdf/$', PDFTemplateView.as_view(template_name='my_template.html',
                                                    filename='my_pdf.pdf'), name='pdf'),
]


