from django import forms

from .models import AcademicSession, AcademicTerm, Grade, ReportTemplate, StudentClass, Subject


class GradeEntryFilterForm(forms.Form):
    student_class = forms.ModelChoiceField(queryset=StudentClass.objects.none())
    subject = forms.ModelChoiceField(queryset=Subject.objects.none())
    session = forms.ModelChoiceField(queryset=AcademicSession.objects.none())
    term = forms.ModelChoiceField(queryset=AcademicTerm.objects.none())

    def __init__(self, *args, class_queryset=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["student_class"].queryset = class_queryset or StudentClass.objects.none()
        self.fields["subject"].queryset = Subject.objects.all()
        self.fields["session"].queryset = AcademicSession.objects.all()
        self.fields["term"].queryset = AcademicTerm.objects.all()


class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ("test_score", "exam_score")
        widgets = {
            "test_score": forms.NumberInput(attrs={"min": 0, "max": 100}),
            "exam_score": forms.NumberInput(attrs={"min": 0, "max": 100}),
        }


class ReportTemplateForm(forms.ModelForm):
    class Meta:
        model = ReportTemplate
        fields = (
            "name",
            "title",
            "intro_text",
            "show_attendance",
            "show_work_habits",
            "show_social_habits",
            "grading_scale_notes",
            "footer_note",
            "is_default",
        )
