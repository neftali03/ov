from django import forms as _forms


class ModelForm(_forms.ModelForm):
    """Custom base `ModelForm`."""

    @property
    def has_files(self):
        """Return True if the form has files."""
        for field in self.fields.values():
            if isinstance(field, _forms.FileField):
                return True
        return False


class Form(_forms.Form):
    """Custom base `Form`."""

    @property
    def has_files(self):
        """Return True if the form has files."""
        for field in self.fields.values():
            if isinstance(field, _forms.FileField):
                return True
        return False
