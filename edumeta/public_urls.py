from django.contrib import admin
from django.urls import path

from tenants import views as tenant_views

urlpatterns = [
    path("", tenant_views.public_landing, name="public_landing"),
    path("admin/", admin.site.urls),
]
