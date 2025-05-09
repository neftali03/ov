from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm as _AuthAuthenticationForm
from django.contrib.auth.forms import UsernameField
from django.contrib.auth.views import LoginView as _LoginView
from django.contrib.auth.views import LogoutView as _LogoutView
from django.shortcuts import redirect
from django.views.decorators.debug import sensitive_variables

from common import forms


class AuthenticationForm(_AuthAuthenticationForm):
    """Custom authentication form for the login page."""

    username = UsernameField(
        label="Usuario",
        widget=forms.TextInput(attrs={"autofocus": True}),
    )
    password = forms.CharField(
        label="Contraseña",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )
    error_messages = {
        "invalid_login": "Credenciales inválidas.",
        "inactive": "Esta cuenta se encuentra inactiva.",
    }


class LoginView(_LoginView):
    """A custom `LoginView`."""

    template_name = "core/login.html"
    authentication_form = AuthenticationForm

    @sensitive_variables("password")
    def form_valid(self, form):
        """Extend to send message upon successful login."""
        response = super().form_valid(form)
        user = form.get_user()
        if not user.is_human:
            logout(self.request)
            return redirect("core:auth:login")
        messages.success(self.request, "Se ha autenticado exitosamente.")
        return response


class LogoutView(_LogoutView):
    """A custom `LogoutView`."""
