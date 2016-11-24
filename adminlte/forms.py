from django import forms


class PageForm(forms.Form):
    title = forms.CharField()
    content = forms.CharField()
