from django.contrib import admin

from .models import Parent, Student, Teacher


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("admission_no", "full_name", "student_class", "gender", "is_active", "grades_visible")
    list_filter = ("is_active", "gender", "student_class", "grades_visible")
    search_fields = ("admission_no", "user__username", "user__first_name", "user__last_name", "user__email")
    autocomplete_fields = ("user", "student_class")
    ordering = ("admission_no",)

    @admin.display(description="Name")
    def full_name(self, obj):
        return obj.user.get_full_name() or obj.user.username


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ("staff_id", "full_name", "specialization", "is_active")
    list_filter = ("is_active", "assigned_classes")
    search_fields = ("staff_id", "user__username", "user__first_name", "user__last_name", "user__email")
    autocomplete_fields = ("user", "assigned_classes")
    ordering = ("staff_id",)

    @admin.display(description="Name")
    def full_name(self, obj):
        return obj.user.get_full_name() or obj.user.username


@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ("full_name", "relation", "occupation")
    list_filter = ("relation",)
    search_fields = ("user__username", "user__first_name", "user__last_name", "user__email")
    autocomplete_fields = ("user", "students")

    @admin.display(description="Name")
    def full_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
