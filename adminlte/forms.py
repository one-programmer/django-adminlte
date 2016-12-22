from django import forms
from django.contrib.auth.models import Permission


class PermissionForm(forms.Form):
    codename = forms.CharField()
    name = forms.CharField()


class GroupForm(forms.Form):
    name = forms.CharField()
    permissions = forms.ModelMultipleChoiceField(queryset=Permission.objects.all(), required=False)
