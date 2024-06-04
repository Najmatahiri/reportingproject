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

import reporting
from reporting.views import MachineVMViewSet, signup, UserLoginView, UserLogoutView, index, ConfigVersionHSViewSet, \
    access_denied, landing_page, logout_view
from django.conf import settings
from django.conf.urls.static import static

# Ici, nous créons notre routeur
router = routers.SimpleRouter()
# Puis lui déclarons une url basée sur le mot clé ‘category’ et notre view
# afin que l’url générée soit celle que nous souhaitons ‘/api/category/’
router.register('machines', MachineVMViewSet, basename='machines')
router.register('config', ConfigVersionHSViewSet, basename='config')

urlpatterns = [
                  path('', landing_page, name='landing_page'),
                  path('waiting-page', index, name="index"),
                  path('access-denied/', access_denied, name='access_denied'),
                  path('reporting/', include('reporting.urls')),
                  path('api-auth/', include('rest_framework.urls')),
                  path('api/', include(router.urls)),
                  path('accounts/signup/', signup, name='signup'),
                  path('accounts/login/', UserLoginView.as_view(), name='login'),
                  path('logout', logout_view, name='logout'),
                  path('accounts/logout/', UserLogoutView.as_view(), name='logout'),
                  path("__debug__/", include("debug_toolbar.urls")),

                  path('admin/', admin.site.urls),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# handler404 = 'reporting.views.handler404'
# handler500 = 'reporting.views.handler500'
