from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.core.exceptions import ValidationError

from common import forms
from config import settings


class UserCreateForm(UserCreationForm):
    """A form to create User."""

    def clean_email(self):
        """Add the validation error to the email."""
        email = self.cleaned_data.get("email")
        if not email:
            raise ValidationError("Debe proporcionar un correo electrónico.")

        domain = email.split("@")[-1]
        if domain not in settings.ALLOWED_USER_EMAIL_DOMAINS:
            raise ValidationError(
                f"El correo electrónico debe pertenecer a uno de estos "
                f"dominios: {', '.join(settings.ALLOWED_USER_EMAIL_DOMAINS)}"
            )
        return email


class UserChangePasswordForm(PasswordChangeForm):
    """A form to change a User's password."""

    new_password1 = forms.CharField(
        label="Nueva contraseña",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text=(
            "Su contraseña no puede asemejarse a su información personal. <br>"
            "Su contraseña debe contener al menos 8 caracteres. <br>"
            "Su contraseña no puede ser una clave utilizada comúnmente. <br>"
            "Su contraseña no puede ser completamente numérica. <br>"
        ),
    )
    new_password2 = forms.CharField(
        label="Nueva contraseña (Confirmación)",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )
    old_password = forms.CharField(
        label="Contraseña temporal",
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", "autofocus": True}
        ),
    )
