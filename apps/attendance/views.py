from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone

from apps.academics.models import StudentClass
from apps.people.models import Parent, Student, Teacher
from .forms import AttendanceFilterForm
from .models import Attendance


def _class_queryset(user):
    if user.is_admin:
        return StudentClass.objects.all()
    if user.is_teacher:
        teacher = Teacher.objects.filter(user=user, is_active=True).first()
        return teacher.assigned_classes.all() if teacher else StudentClass.objects.none()
    return StudentClass.objects.none()


def _student_queryset(user, student_class=None):
    if user.is_admin:
        students = Student.objects.select_related("user", "student_class").all()
    elif user.is_teacher:
        classes = _class_queryset(user)
        students = Student.objects.select_related("user", "student_class").filter(student_class__in=classes)
    elif user.is_parent:
        parent = Parent.objects.filter(user=user).first()
        students = parent.students.select_related("user", "student_class") if parent else Student.objects.none()
    elif user.is_student:
        students = Student.objects.select_related("user", "student_class").filter(user=user)
    else:
        students = Student.objects.none()

    if student_class:
        students = students.filter(student_class=student_class)
    return students.filter(is_active=True).distinct()


@login_required
def index(request):
    class_queryset = _class_queryset(request.user)
    selected_class = None
    selected_date = timezone.localdate()
    students = Student.objects.none()
    records_by_student = {}
    attendance_rows = []
    attendance_history = Attendance.objects.none()

    if request.user.is_admin or request.user.is_teacher:
        data = request.POST if request.method == "POST" else request.GET
        form = AttendanceFilterForm(data or None, class_queryset=class_queryset)
        if form.is_valid():
            selected_class = form.cleaned_data["student_class"]
            selected_date = form.cleaned_data["date"]
            students = _student_queryset(request.user, selected_class)

            if request.method == "POST":
                for student in students:
                    status = request.POST.get(f"status_{student.id}", "present")
                    remarks = request.POST.get(f"remarks_{student.id}", "")
                    if status not in dict(Attendance.STATUS_CHOICES):
                        continue
                    Attendance.objects.update_or_create(
                        student=student,
                        date=selected_date,
                        defaults={
                            "student_class": selected_class,
                            "status": status,
                            "remarks": remarks,
                        },
                    )
                messages.success(request, "Attendance saved.")
                url = f"{reverse('attendance:index')}?student_class={selected_class.id}&date={selected_date.isoformat()}"
                return redirect(url)

            records_by_student = {
                record.student_id: record
                for record in Attendance.objects.filter(student__in=students, date=selected_date)
            }
            attendance_rows = [
                {"student": student, "record": records_by_student.get(student.id)}
                for student in students
            ]
    else:
        form = None
        students = _student_queryset(request.user)
        attendance_history = (
            Attendance.objects.filter(student__in=students)
            .select_related("student", "student__user", "student_class")
            .order_by("-date", "student__admission_no")[:80]
        )

    return render(
        request,
        "attendance/index.html",
        {
            "page_title": "Attendance",
            "active_section": "attendance",
            "form": form,
            "students": students,
            "selected_class": selected_class,
            "selected_date": selected_date,
            "attendance_rows": attendance_rows,
            "attendance_history": attendance_history,
            "status_choices": Attendance.STATUS_CHOICES,
        },
    )
