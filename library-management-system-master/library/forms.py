from django import forms
from .models import Student, Issue, Books, Librarian
from django.contrib.auth.models import User
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class StudentForm(forms.ModelForm):
    gender = forms.ChoiceField(choices=Student.GENDER_CHOICES)
    department = forms.ChoiceField(choices=Student.BRANCH_CHOICES)
    semester = forms.ChoiceField(choices=Student.SEMESTER_CHOICES)
    class Meta:
        model = Student
        exclude = ['user', 'fullname']

class BookForm(forms.ModelForm):
    class Meta:
        model = Books
        fields = ('book_id', 'title', 'author', 'isbn', 'publisher')    

class StaffForm(forms.ModelForm):
    class Meta:
        model = Librarian
        exclude = ['user', 'fullname']