from django.db import models
from django_tenants.models import TenantMixin, DomainMixin


class School(TenantMixin):
    name = models.CharField(max_length=200)
    subdomain_slug = models.SlugField(unique=True)  # e.g. "ramoth"
    created_on = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    # django-tenants requires this — auto-creates/drops schema on save/delete
    auto_create_schema = True
    auto_drop_schema = True

    def __str__(self):
        return self.name


class Domain(DomainMixin):
    pass