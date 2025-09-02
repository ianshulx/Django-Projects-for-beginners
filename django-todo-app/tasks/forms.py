from django import forms
from django.utils import timezone

from .models import Task


class TaskForm(forms.ModelForm):
    due_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}), required=False
    )

    class Meta:
        model = Task
        fields = ["title", "description", "is_completed", "priority", "due_date"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "priority": forms.Select(attrs={"class": "form-select"}),
            "due_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "is_completed": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def clean_due_date(self):
        due_date = self.cleaned_data.get("due_date")
        if due_date and due_date < timezone.now().date():
            raise forms.ValidationError("The date of entry cannot be in the past.")
        return due_date
