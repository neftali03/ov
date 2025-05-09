from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse
from django.shortcuts import redirect, render

from apps.core.forms import user as forms
from apps.core.services import user as sv
from common import http
from common.decorators import require_GET_POST


@require_GET_POST
def change_password(request) -> HttpResponse:
    """Display and handle a User change password page."""
    if request.method == "POST":
        form = forms.UserChangePasswordForm(user=request.user, data=request.POST)
        old_password = request.POST.get("old_password")
        new_password1 = request.POST.get("new_password1")
        new_password2 = request.POST.get("new_password2")

        if form.is_valid():
            if not (old_password == new_password1 and old_password == new_password2):
                # noinspection PyUnresolvedReferences
                if not any(
                    check_password(new_password1, password)
                    for password in request.user.previous_password
                ):
                    # noinspection PyTypeChecker
                    sv.change_password(
                        request.user,
                        form.cleaned_data["new_password2"],
                    )
                    messages.success(request, "Contraseña cambiada exitosamente")
                    return redirect("core:index")
                else:
                    message = "Ya ha utilizado recientemente esta contraseña."
                    form.add_error(None, message)
            else:
                message = (
                    "La nueva contraseña no puede ser "
                    "igual a la contraseña temporal."
                )
                form.add_error(None, message)
        status_code = http.HttpCodes.FORM_INVALID
    else:
        form = forms.UserChangePasswordForm(user=request.user)
        status_code = http.HttpCodes.OK

    return render(
        request,
        template_name="core/user/change_password.html",
        status=status_code,
        context={"page_title": "Cambiar contraseña", "form": form},
    )
