from django.conf import settings
from django.contrib import messages
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import redirect

from common.http import reverse


class LoginRequiredMiddleware:
    """
    Enforce authentication on all requests.

    Otherwise, redirect to login page, except for API requests
    which will be handled downstream by DRF auth policy.
    This middleware must be placed after the Authentication middleware.
    """

    def __init__(self, get_response):
        """Extend `init` method."""
        self.get_response = get_response

    def __call__(self, request):
        """Redirect unauthenticated users to the login page."""
        is_login = request.path_info == settings.LOGIN_URL
        is_api = settings.API_URL in request.path_info
        is_authenticated = request.user.is_authenticated

        if is_authenticated and is_login:
            return redirect("core:index")

        if is_authenticated or is_api or is_login:
            return self.get_response(request)

        return redirect_to_login(request.path)


class TempPasswordMiddleware:
    """Redirects users to change password if it is temp."""

    def __init__(self, get_response):
        """Extend `init` method."""
        self.get_response = get_response

    def __call__(self, request):
        """Redirect unauthenticated users to the login page."""
        if (
            request.user.is_authenticated
            and request.user.tmp_password
            and request.user.is_human
            and not any(
                [
                    request.path_info == reverse("core:user:change_password"),
                    request.path_info == reverse("core:auth:logout"),
                    settings.API_URL in request.path_info,
                ]
            )
        ):
            message = "Su contraseña es temporal y debe actualizarla"
            messages.warning(request, message)
            return redirect("core:user:change_password")

        return self.get_response(request)
