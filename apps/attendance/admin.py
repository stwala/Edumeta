from django.contrib import admin

from .models import Attendance


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("student", "student_class", "date", "status")
    list_filter = ("status", "date", "student_class")
    search_fields = ("student__admission_no", "student__user__first_name", "student__user__last_name")
    autocomplete_fields = ("student", "student_class")
    date_hierarchy = "date"
    ordering = ("-date", "student")
