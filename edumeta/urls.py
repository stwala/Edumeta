from django.contrib import admin
from django.urls import include, path

from edumeta import views as core_views

urlpatterns = [
    path("", core_views.dashboard, name="dashboard"),
    path("accounts/", include("apps.accounts.urls")),
    path("academics/", include("apps.academics.urls")),
    path("people/", include("apps.people.urls")),
    path("attendance/", include("apps.attendance.urls")),
    path("finance/", include("apps.finance.urls")),
    path("admin/", admin.site.urls),
]
