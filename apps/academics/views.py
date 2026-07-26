from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse

from apps.accounts.decorators import role_required
from apps.attendance.models import Attendance
from apps.people.models import Parent, Student, Teacher
from .forms import GradeEntryFilterForm, ReportTemplateForm
from .models import Grade, ReportTemplate, StudentClass


def _page(request, template, title, section):
    return render(
        request,
        template,
        {"page_title": title, "active_section": section},
    )


def _class_queryset(user):
    if user.is_admin:
        return StudentClass.objects.all()
    if user.is_teacher:
        teacher = Teacher.objects.filter(user=user, is_active=True).first()
        return teacher.assigned_classes.all() if teacher else StudentClass.objects.none()
    return StudentClass.objects.none()


def _visible_students(user, student_class=None):
    if user.is_admin:
        students = Student.objects.select_related("user", "student_class").all()
    elif user.is_teacher:
        students = Student.objects.select_related("user", "student_class").filter(student_class__in=_class_queryset(user))
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


def _default_report_template():
    template, _ = ReportTemplate.objects.get_or_create(
        is_default=True,
        defaults={"name": "Default report"},
    )
    return template


def _score_from_post(request, field_name):
    try:
        score = int(request.POST.get(field_name) or 0)
    except ValueError:
        return 0
    return max(0, min(score, 100))


@login_required
def index(request):
    return _page(request, "academics/index.html", "Academics", "academics")


@role_required("admin", "teacher")
def sessions(request):
    return _page(request, "academics/sessions.html", "Sessions & terms", "academics")


@role_required("admin", "teacher")
def classes(request):
    return _page(request, "academics/classes.html", "Classes & subjects", "academics")


@login_required
def reports(request):
    user = request.user
    class_queryset = _class_queryset(user)
    report_template = _default_report_template()
    template_form = ReportTemplateForm(instance=report_template)
    filter_form = None
    grade_rows = []
    visible_grades = Grade.objects.none()
    attendance_summary = []

    if request.method == "POST" and user.is_admin and request.POST.get("action") == "save_template":
        template_form = ReportTemplateForm(request.POST, instance=report_template)
        if template_form.is_valid():
            template_form.save()
            messages.success(request, "Report template updated for this school.")
            return redirect("academics:reports")

    if user.is_admin or user.is_teacher:
        data = request.POST if request.method == "POST" and request.POST.get("action") == "save_grades" else request.GET
        filter_form = GradeEntryFilterForm(data or None, class_queryset=class_queryset)
        if filter_form.is_valid():
            student_class = filter_form.cleaned_data["student_class"]
            subject = filter_form.cleaned_data["subject"]
            session = filter_form.cleaned_data["session"]
            term = filter_form.cleaned_data["term"]
            students = _visible_students(user, student_class)

            if request.method == "POST" and request.POST.get("action") == "save_grades":
                for student in students:
                    Grade.objects.update_or_create(
                        student=student,
                        subject=subject,
                        session=session,
                        term=term,
                        defaults={
                            "student_class": student_class,
                            "test_score": _score_from_post(request, f"test_score_{student.id}"),
                            "exam_score": _score_from_post(request, f"exam_score_{student.id}"),
                        },
                    )
                messages.success(request, "Grades saved.")
                url = (
                    f"{reverse('academics:reports')}?student_class={student_class.id}"
                    f"&subject={subject.id}&session={session.id}&term={term.id}"
                )
                return redirect(url)

            existing_grades = {
                grade.student_id: grade
                for grade in Grade.objects.filter(
                    student__in=students,
                    subject=subject,
                    session=session,
                    term=term,
                )
            }
            grade_rows = [
                {"student": student, "grade": existing_grades.get(student.id)}
                for student in students
            ]
    else:
        students = _visible_students(user)
        if user.is_parent:
            students = students.filter(grades_visible=True)
        visible_grades = (
            Grade.objects.filter(student__in=students)
            .select_related("student", "student__user", "subject", "session", "term", "student_class")
            .order_by("-session__name", "term__name", "student__admission_no", "subject__name")
        )
        for student in students:
            attendance_summary.append(
                {
                    "student": student,
                    "present": Attendance.objects.filter(student=student, status="present").count(),
                    "late": Attendance.objects.filter(student=student, status="late").count(),
                    "absent": Attendance.objects.filter(student=student, status="absent").count(),
                }
            )

    return render(
        request,
        "academics/reports.html",
        {
            "page_title": "Reports & grades",
            "active_section": "academics",
            "filter_form": filter_form,
            "grade_rows": grade_rows,
            "visible_grades": visible_grades,
            "attendance_summary": attendance_summary,
            "report_template": report_template,
            "template_form": template_form,
        },
    )
