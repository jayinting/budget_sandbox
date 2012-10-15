from django import forms

class SampleForm(forms.Form):

    #name = forms.CharField(max_length=255)
    file = forms.FileField()
