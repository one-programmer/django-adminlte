from django import forms


class PermissionForm(forms.Form):
    codename = forms.CharField()
    name = forms.CharField()
