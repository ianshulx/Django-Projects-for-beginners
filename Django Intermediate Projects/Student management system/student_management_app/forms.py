from django import forms 
from django.forms import Form
from student_management_app.models import Courses, SessionYearModel


class DateInput(forms.DateInput):
    input_type = "date"


class AddStudentForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class":"form-control"}))
    password = forms.CharField(label="Password", max_length=50, widget=forms.PasswordInput(attrs={"class":"form-control"}))
    first_name = forms.CharField(label="First Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    address = forms.CharField(label="Address", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))

    gender_list = (
        ('Male','Male'),
        ('Female','Female')
    )

    course_id = forms.ChoiceField(
        label="Course",
        choices=[],
        widget=forms.Select(attrs={"class":"form-control"})
    )

    gender = forms.ChoiceField(
        label="Gender",
        choices=gender_list,
        widget=forms.Select(attrs={"class":"form-control"})
    )

    session_year_id = forms.ChoiceField(
        label="Session Year",
        choices=[],
        widget=forms.Select(attrs={"class":"form-control"})
    )

    profile_pic = forms.FileField(
        label="Profile Pic",
        required=False,
        widget=forms.FileInput(attrs={"class":"form-control"})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['course_id'].choices = [
            (course.id, course.course_name)
            for course in Courses.objects.all()
        ]

        self.fields['session_year_id'].choices = [
            (
                session.id,
                f"{session.session_start_year} to {session.session_end_year}"
            )
            for session in SessionYearModel.objects.all()
        ]

class EditStudentForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class":"form-control"}))
    first_name = forms.CharField(label="First Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    address = forms.CharField(label="Address", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))

    gender_list = (
        ('Male','Male'),
        ('Female','Female')
    )

    course_id = forms.ChoiceField(
        label="Course",
        choices=[],
        widget=forms.Select(attrs={"class":"form-control"})
    )

    gender = forms.ChoiceField(
        label="Gender",
        choices=gender_list,
        widget=forms.Select(attrs={"class":"form-control"})
    )

    session_year_id = forms.ChoiceField(
        label="Session Year",
        choices=[],
        widget=forms.Select(attrs={"class":"form-control"})
    )

    profile_pic = forms.FileField(
        label="Profile Pic",
        required=False,
        widget=forms.FileInput(attrs={"class":"form-control"})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['course_id'].choices = [
            (course.id, course.course_name)
            for course in Courses.objects.all()
        ]

        self.fields['session_year_id'].choices = [
            (
                session.id,
                f"{session.session_start_year} to {session.session_end_year}"
            )
            for session in SessionYearModel.objects.all()
        ]