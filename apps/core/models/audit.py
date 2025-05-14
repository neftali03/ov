from django.conf import settings
from django.contrib.postgres.functions import TransactionNow
from django.db.models import Model as _Model

from common.models import fields

USER_MODEL = settings.AUTH_USER_MODEL


class _RequestLogBase(_Model):
    """Audit log for HTTP requests."""

    remote_ip = fields.CharField(max_length=20)
    url = fields.TextField(blank=True)
    method = fields.CharField(max_length=10)
    response_code = fields.PositiveSmallIntegerField()
    execution_time_ms = fields.IntegerField()
    user = fields.ForeignKey(USER_MODEL, null=True)  # type: ignore
    created_at = fields.DateTimeField(default=TransactionNow())

    class Meta:  # noqa: D106
        abstract = True


class RequestLog(_RequestLogBase):
    """Audit log for HTTP requests."""

    class Meta:  # noqa: D106
        verbose_name = "Registro de petición"
        verbose_name_plural = "Registro de peticiones"
        permissions = [("view_request_log", "Ver registro de peticiones")]


class RequestLogHistorical(_RequestLogBase):
    """Audit log for HTTP requests."""

    class Meta:  # noqa: D106
        verbose_name = "Registro histórico de petición"
        verbose_name_plural = "Registro histórico de peticiones"
        permissions = [
            ("view_request_log_historical", "Ver registro histórico de peticiones"),
        ]


class _ActionLogBase(_Model):
    """Audit log for a model actions populated via database triggers."""

    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"

    ACTIONS = [
        ("CREATE", "Crear"),
        ("UPDATE", "Actualizar"),
        ("DELETE", "Eliminar"),
    ]

    db_user = fields.TextField()
    db_schema = fields.TextField()
    db_table = fields.TextField()
    action = fields.TextField(choices=ACTIONS)
    model_id = fields.PositiveBigIntegerField()
    old_data = fields.JSONField(null=True)
    new_data = fields.JSONField(null=True)
    created_at = fields.DateTimeField(default=TransactionNow())

    class Meta:  # noqa: D106
        abstract = True


class ActionLog(_ActionLogBase):
    """Audit log for a model actions populated via database triggers."""

    class Meta:  # noqa: D106
        verbose_name = "Registro de acción"
        verbose_name_plural = "Registro de acciones"
        permissions = [("view_action_log", "Ver registro de acciones")]


class ActionLogHistorical(_ActionLogBase):
    """Audit log for a model actions populated via database triggers."""

    class Meta:  # noqa: D106
        verbose_name = "Registro histórico de acción"
        verbose_name_plural = "Registro histórico de acciones"
        permissions = [
            ("view_action_log_historical", "Ver registro histórico de acciones"),
        ]
