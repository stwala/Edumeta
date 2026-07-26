from django.contrib import admin
from django.db import connection
from django_tenants.utils import get_public_schema_name

from .models import School, Domain


class PublicSchemaOnlyAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return connection.schema_name == get_public_schema_name()

    def has_view_permission(self, request, obj=None):
        return connection.schema_name == get_public_schema_name() and super().has_view_permission(request, obj)

    def has_add_permission(self, request):
        return connection.schema_name == get_public_schema_name() and super().has_add_permission(request)

    def has_change_permission(self, request, obj=None):
        return connection.schema_name == get_public_schema_name() and super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        return connection.schema_name == get_public_schema_name() and super().has_delete_permission(request, obj)


@admin.register(School)
class SchoolAdmin(PublicSchemaOnlyAdmin):
    list_display = ("name", "schema_name", "subdomain_slug", "is_active", "created_on")
    list_filter = ("is_active", "created_on")
    search_fields = ("name", "schema_name", "subdomain_slug")


@admin.register(Domain)
class DomainAdmin(PublicSchemaOnlyAdmin):
    list_display = ("domain", "tenant", "is_primary")
    list_filter = ("is_primary",)
    search_fields = ("domain", "tenant__name", "tenant__schema_name")
