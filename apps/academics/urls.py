from django.urls import path

from . import views

app_name = "academics"

urlpatterns = [
    path("", views.index, name="index"),
    path("sessions/", views.sessions, name="sessions"),
    path("classes/", views.classes, name="classes"),
    path("reports/", views.reports, name="reports"),
]
