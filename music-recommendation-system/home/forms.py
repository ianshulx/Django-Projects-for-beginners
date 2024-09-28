from django import forms

class inputform(forms.Form):
    fav_music = forms.CharField(label='fav_music', max_length=50)
    