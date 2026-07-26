from django import forms
from django.utils import timezone

from apps.academics.models import StudentClass


class AttendanceFilterForm(forms.Form):
    student_class = forms.ModelChoiceField(queryset=StudentClass.objects.none())
    date = forms.DateField(
        initial=timezone.localdate,
        widget=forms.DateInput(attrs={"type": "date"}),
    )

    def __init__(self, *args, class_queryset=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["student_class"].queryset = class_queryset or StudentClass.objects.none()
