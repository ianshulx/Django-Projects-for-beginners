from django import forms

class UrlForm(forms.Form):
    link = forms.CharField(max_length=1000)