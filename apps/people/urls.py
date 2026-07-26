from django.urls import path

from . import views

app_name = "people"

urlpatterns = [
    path("", views.index, name="index"),
    path("students/", views.students, name="students"),
    path("teachers/", views.teachers, name="teachers"),
    path("parents/", views.parents, name="parents"),
]
