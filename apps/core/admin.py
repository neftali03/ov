from django import forms
from django.conf import settings
from django.contrib import admin, messages
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm as _UserChangeForm
from django.core.mail import send_mail
from django.utils.translation import ngettext

from apps.core.forms.user import UserCreateForm
from apps.core.models import RequestLog
from common import functions as fn

admin.site.site_title = "Admin"
admin.site.site_header = "OV Administration"
admin.site.index_title = "Orientación vocacional"

User = get_user_model()


class UserChangeForm(_UserChangeForm):
    """Custom user change form."""

    class Meta:  # noqa: D106
        model = User
        fields = "__all__"


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom user admin."""

    add_form = UserCreateForm
    form = UserChangeForm
    # noinspection PyUnresolvedReferences
    fieldsets = list(BaseUserAdmin.fieldsets or []) + [
        (
            "Additional info",
            {
                "fields": (
                    "is_human",
                    "is_management",
                )
            },
        ),
    ]
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2", "email"),
            },
        ),
    )

    def get_form(self, request, instance=None, **kwargs):
        """Add a temporary password automatically."""
        form = super().get_form(request, instance, **kwargs)
        if not instance:
            password = fn.make_random_password()
            form.base_fields["password1"].initial = password
            form.base_fields["password2"].initial = password
            form.base_fields["password1"].widget = forms.HiddenInput()
            form.base_fields["password2"].widget = forms.HiddenInput()
        return form

    def save_model(self, request, instance, form, change):
        """Create a new user and send an email."""
        if not change:
            new_password = form.cleaned_data.get("password1")
            instance.set_password(new_password)
            instance.save(request.user.id)
            if self.send_tmp_password_email(request, instance, new_password):
                message = (
                    f"La contraseña de {instance.username} "
                    f"fue enviada por correo electrónico exitosamente."
                )
                messages.success(request, message)
            else:
                instance.tmp_password = False
                instance.save(update_fields=["tmp_password"])
        else:
            instance.save(request.user.id)

    actions = ["reset_password"]

    @admin.action(description="Reset password")
    def reset_password(self, request, queryset):
        """Assign temporary password to selected users."""
        updated = 0
        for instance in queryset:
            new_password = fn.make_random_password()
            if not instance.email:
                message = (
                    f"No se puede resetear la contraseña de {instance.username} "
                    f"porque no posee un correo electrónico."
                )
                messages.error(request, message)
                instance.save(request.user.id)

            else:
                if instance.tmp_password:
                    message = (
                        f"El usuario {instance.username} ya se le había enviado "
                        f"un correo electrónico con su contraseña temporal."
                    )
                    messages.warning(request, message)
                instance.set_password(new_password)
                instance.tmp_password = True

                if self.send_tmp_password_email(request, instance, new_password):
                    instance.save(request.user.id)
                    updated += 1
                else:
                    instance.tmp_password = False
                    instance.save(request.user.id)

        if updated > 0:
            self.message_user(
                request,
                ngettext(
                    "%d The temporary passwords was sent.",
                    "%d The temporary passwords were sent.",
                    updated,
                )
                % updated,
                messages.SUCCESS,
            )

    # noinspection PyMethodMayBeStatic
    def send_tmp_password_email(self, request, instance, new_password):
        """Send an email with the temporary password."""
        subject = "OV | Credenciales"
        message = (
            f"Hola {instance.username},\n\n"
            f"Te comparto tus nuevos datos para que puedas acceder a "
            f"nuestro sitio de orientación vocacional.\n\n"
            f"Al iniciar sesión, el sistema te pedirá que cambies la contraseña, "
            f"ya que la que tienes actualmente es temporal. "
            f"Por favor, asegúrate de establecer una contraseña que recuerdes.\n\n\n"
            f"~~~~ Datos de acceso ~~~~\n\n"
            f"Usuario: {instance.username}\n"
            f"Contraseña temporal: {new_password}\n\n"
            f"Ante cualquier duda o consulta, no dudes en "
            f"contactar al administrador.\n\n"
            "Saludos, \n\nOV"
        )
        try:
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [instance.email],
                fail_silently=False,
            )
            return True
        except Exception as e:
            messages.error(
                request, f"Error al enviar el correo a {instance.username}: {str(e)}"
            )
            return False


@admin.register(RequestLog)
class RequestLogAdmin(admin.ModelAdmin):
    """Model admin."""

    list_display = (
        "remote_ip",
        "url",
        "method",
        "response_code",
        "execution_time_ms",
        "user",
        "created_at",
    )
    list_filter = (
        "method",
        "response_code",
        "user",
        "created_at",
    )
    # noinspection PyUnresolvedReferences
    search_fields = ("remote_ip", "url", "method", "response_code", "user__username")
