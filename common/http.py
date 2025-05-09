from enum import Enum, IntEnum
from typing import Literal

from django.http import HttpResponse
from django.urls import reverse as _reverse
from django.utils.functional import lazy
from django_htmx.http import trigger_client_event


class HttpCodes(IntEnum):
    """HTTP Status codes."""

    OK = 200
    NO_CONTENT = 204
    FORM_INVALID = 422
    BAD_REQUEST = 400
    SERVER_ERROR = 500
    NOT_FOUND = 404


class StrEnum(str, Enum):
    """String-based Enum for consistent serialization."""

    pass


class DefaultMessage(StrEnum):
    """Default messages."""

    FORM_ERROR = "Por favor corrija los errores de la forma."
    ACTION_ERROR = "La acción no pudo ser ejecutada."
    NO_PERMISSION = "No tiene permiso para ejecutar esta acción."
    SEARCH_ERROR = "Hubo un error durante la búsqueda. Intente de nuevo."
    DOWNLOAD_ERROR = "Hubo un error durante la descarga. Intente de nuevo."


def trigger_htmx_message(
    response: HttpResponse,
    message: str,
    level: int,
    after: Literal["receive", "settle", "swap"] = "swap",
) -> HttpResponse:
    """Return the response with an HTMX message trigger."""
    return trigger_client_event(
        response,
        "showHtmxMessage",
        {"content": message, "level": level},
        after=after,
    )


def reverse(view_name: str, *args, urlconf=None, current_app=None, **kwargs):
    """Extend built-in function for dev quality of life."""
    return _reverse(
        view_name,
        urlconf=urlconf,
        current_app=current_app,
        args=args,
        kwargs=kwargs,
    )


reverse_lazy = lazy(reverse, str)
