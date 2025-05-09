from django import forms


class CharField(forms.CharField):
    """Custom `CharField`."""


class TextField(CharField):
    """Custom `TextField`."""
