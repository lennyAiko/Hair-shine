"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework_swagger.views import get_swagger_view
from rest_framework.schemas import get_schema_view as gsv

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    # admin
    re_path(r'^lenny/', admin.site.urls),

    path('api-auth/', include('rest_framework.urls')),

    # custom apps
    path('accounts/', include('account.urls')),
    path('store/', include('store.urls')),

    # swagger
    path('swagger/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/schema/docs/',
         SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
