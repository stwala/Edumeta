from django.contrib import admin

from .models import AcademicSession, AcademicTerm, Grade, ReportTemplate, StudentClass, StudentTermReport, Subject


@admin.register(AcademicSession)
class AcademicSessionAdmin(admin.ModelAdmin):
    list_display = ("name", "current")
    list_filter = ("current",)
    search_fields = ("name",)
    ordering = ("-name",)


@admin.register(AcademicTerm)
class AcademicTermAdmin(admin.ModelAdmin):
    list_display = ("name", "current")
    list_filter = ("current",)
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name", "code")
    search_fields = ("name", "code")
    ordering = ("name",)


@admin.register(StudentClass)
class StudentClassAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name", "subjects__name")
    autocomplete_fields = ("subjects",)
    ordering = ("name",)


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ("student", "subject", "student_class", "session", "term", "test_score", "exam_score", "total_score", "grade_letter")
    list_filter = ("session", "term", "student_class", "subject")
    search_fields = ("student__admission_no", "student__user__first_name", "student__user__last_name", "subject__name")
    autocomplete_fields = ("student", "subject", "session", "term", "student_class")


@admin.register(StudentTermReport)
class StudentTermReportAdmin(admin.ModelAdmin):
    list_display = ("student", "session", "term", "student_class", "promotion_status")
    list_filter = ("session", "term", "student_class", "promotion_status")
    search_fields = ("student__admission_no", "student__user__first_name", "student__user__last_name")
    autocomplete_fields = ("student", "session", "term", "student_class")


@admin.register(ReportTemplate)
class ReportTemplateAdmin(admin.ModelAdmin):
    list_display = ("name", "title", "is_default", "updated_at")
    list_filter = ("is_default",)
    search_fields = ("name", "title")
