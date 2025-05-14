from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.functions import TransactionNow
from django.db import models as _models

from common.models.fields import BooleanField, DateTimeField, ForeignKey
from config import settings


class User(AbstractUser):
    """Extended custom user."""

    is_human = BooleanField(
        verbose_name="Is the user human?",
        default=True,
    )
    is_management = BooleanField(
        verbose_name="Is the user on the top management?",
        default=False,
    )
    tmp_password = BooleanField(default=True)
    previous_password = ArrayField(
        _models.CharField(max_length=128),
        size=settings.PASSWORD_HISTORY,
        default=list,
        blank=True,
    )
    created_at = DateTimeField(
        verbose_name="Creado",
        default=TransactionNow(),
    )
    created_by = ForeignKey(  # type: ignore
        "self",
        on_delete=_models.PROTECT,
        verbose_name="Creado por",
        related_name="created_users",
        editable=False,
        null=True,
    )
    updated_at = DateTimeField(
        verbose_name="Actualizado",
        default=TransactionNow(),
    )
    updated_by = ForeignKey(  # type: ignore
        "self",
        on_delete=_models.PROTECT,
        verbose_name="Actualizado por",
        related_name="updated_users",
        editable=False,
        null=True,
    )

    def save(self, user_id=None, *args, **kwargs):
        """Extend to include extra functionality."""
        if self.pk is None:
            self.created_by_id = user_id
        self.updated_by_id = user_id

        super().save(*args, **kwargs)

    def push_password_history(self, new_password):
        """Push password to history."""
        if len(self.previous_password) >= settings.PASSWORD_HISTORY:
            self.previous_password.pop(0)
        self.previous_password.append(new_password)
