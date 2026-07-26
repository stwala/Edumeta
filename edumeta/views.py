from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from apps.academics.models import Grade, StudentClass
from apps.attendance.models import Attendance
from apps.people.models import Parent, Student, Teacher


def _teacher_profile(user):
    return Teacher.objects.filter(user=user, is_active=True).first()


def _parent_profile(user):
    return Parent.objects.filter(user=user).first()


@login_required
def dashboard(request):
    user = request.user
    stats = []
    actions = []
    recent_grades = Grade.objects.none()
    recent_attendance = Attendance.objects.none()

    if user.is_admin:
        stats = [
            ("Students", Student.objects.filter(is_active=True).count(), "people:students"),
            ("Teachers", Teacher.objects.filter(is_active=True).count(), "people:teachers"),
            ("Classes", StudentClass.objects.count(), "academics:classes"),
            ("Attendance records", Attendance.objects.count(), "attendance:index"),
        ]
        actions = [
            ("Manage users and roles", "admin:accounts_user_changelist"),
            ("Review students", "people:students"),
            ("Set report template", "academics:reports"),
        ]
    elif user.is_teacher:
        teacher = _teacher_profile(user)
        classes = teacher.assigned_classes.all() if teacher else StudentClass.objects.none()
        students = Student.objects.filter(student_class__in=classes, is_active=True).distinct()
        stats = [
            ("Assigned classes", classes.count(), "academics:classes"),
            ("My students", students.count(), "people:students"),
            ("Attendance records", Attendance.objects.filter(student__in=students).count(), "attendance:index"),
            ("Grades entered", Grade.objects.filter(student__in=students).count(), "academics:reports"),
        ]
        actions = [
            ("Mark attendance", "attendance:index"),
            ("Enter grades", "academics:reports"),
            ("View my students", "people:students"),
        ]
    elif user.is_parent:
        parent = _parent_profile(user)
        children = parent.students.filter(is_active=True) if parent else Student.objects.none()
        recent_grades = Grade.objects.filter(student__in=children).select_related("student", "subject", "term", "session")[:5]
        recent_attendance = Attendance.objects.filter(student__in=children).select_related("student", "student_class")[:5]
        stats = [
            ("Linked students", children.count(), "people:students"),
            ("Published grades", recent_grades.count(), "academics:reports"),
            ("Attendance updates", recent_attendance.count(), "attendance:index"),
        ]
        actions = [
            ("View grades", "academics:reports"),
            ("View attendance", "attendance:index"),
        ]
    else:
        stats = [
            ("Profile", "Ready", "dashboard"),
        ]

    return render(
        request,
        "dashboard/home.html",
        {
            "page_title": "Dashboard",
            "active_section": "dashboard",
            "stats": stats,
            "actions": actions,
            "recent_grades": recent_grades,
            "recent_attendance": recent_attendance,
        },
    )
