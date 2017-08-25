from django import forms

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    type = forms.CharField(max_length=50)
    tag = forms.CharField(max_length=50)
    keyword = forms.CharField(max_length=50)
    file = forms.FileField()