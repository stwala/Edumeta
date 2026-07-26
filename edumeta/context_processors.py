from django.db import connection
from django_tenants.utils import get_public_schema_name

from edumeta.navigation import NAV_ITEMS


def _role(user):
    if not user.is_authenticated:
        return None
    return getattr(user, "role", None)


def _filter_by_role(items, role):
    if role is None:
        return []
    out = []
    for item in items:
        if role not in item.get("roles", ()):
            continue
        entry = {k: v for k, v in item.items() if k != "children"}
        children = item.get("children")
        if children:
            entry["children"] = [
                c for c in children if role in c.get("roles", ())
            ]
        out.append(entry)
    return out


def tenant_branding(request):
    tenant = getattr(request, "tenant", None)
    on_public = connection.schema_name == get_public_schema_name()
    name = "EduMeta"
    if tenant and getattr(tenant, "name", None):
        name = tenant.name
    return {
        "current_tenant": tenant,
        "is_public_schema": on_public,
        "school_name": name,
    }


def sidebar_navigation(request):
    role = _role(request.user)
    return {
        "nav_items": _filter_by_role(NAV_ITEMS, role),
    }
