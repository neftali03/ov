from cfgv import ValidationError
from django.utils.translation import gettext as _

from apps.core.models import User


def change_password(user: User, password: str) -> None:
    """Change a User's password."""
    if user.is_superuser:
        raise ValidationError(_("Forbidden action."))
    user.tmp_password = False
    user.set_password(password)
    user.push_password_history(user.password)
    user.save(user.id)
