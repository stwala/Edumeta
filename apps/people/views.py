from django.shortcuts import render

from apps.accounts.decorators import role_required
from .models import Parent, Student, Teacher


def _page(request, template, title):
    return render(
        request,
        template,
        {"page_title": title, "active_section": "people"},
    )


def _visible_students(user):
    if user.is_admin:
        return Student.objects.select_related("user", "student_class").all()
    if user.is_teacher:
        teacher = Teacher.objects.filter(user=user, is_active=True).first()
        if not teacher:
            return Student.objects.none()
        return Student.objects.select_related("user", "student_class").filter(
            student_class__in=teacher.assigned_classes.all(),
            is_active=True,
        ).distinct()
    if user.is_parent:
        parent = Parent.objects.filter(user=user).first()
        if not parent:
            return Student.objects.none()
        return parent.students.select_related("user", "student_class").filter(is_active=True)
    if user.is_student:
        return Student.objects.select_related("user", "student_class").filter(user=user, is_active=True)
    return Student.objects.none()


@role_required("admin", "teacher", "parent", "student")
def index(request):
    students = _visible_students(request.user)
    return render(
        request,
        "people/index.html",
        {
            "page_title": "People",
            "active_section": "people",
            "students": students,
        },
    )


@role_required("admin", "teacher", "parent", "student")
def students(request):
    return render(
        request,
        "people/students.html",
        {
            "page_title": "Students",
            "active_section": "people",
            "students": _visible_students(request.user),
        },
    )


@role_required("admin")
def teachers(request):
    return _page(request, "people/teachers.html", "Teachers")


@role_required("admin", "teacher")
def parents(request):
    parents = Parent.objects.select_related("user").prefetch_related("students__user")
    if request.user.is_teacher:
        students = _visible_students(request.user)
        parents = parents.filter(students__in=students).distinct()
    return render(
        request,
        "people/parents.html",
        {
            "page_title": "Parents",
            "active_section": "people",
            "parents": parents,
        },
    )
