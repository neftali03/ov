from typing import Literal, Optional

from django.forms import widgets

EMAIL_WIDGET_ATTRS = {"type": "email", "dx-case": "lower", "pattern": ".+\\.[a-z]{2,}$"}


class PasswordInput(widgets.PasswordInput):
    """Custom `Password` widget."""


class TextInput(widgets.TextInput):
    """Custom `TextInput` widget."""

    def __init__(
        self,
        attrs=None,
        case: Optional[Literal["upper", "lower"]] = None,
        pattern: Optional[str] = None,
        autofocus: bool = False,
        numeric: bool = False,
        email: bool = False,
    ):
        """Extend to customize behaviour."""
        attrs = attrs or {}
        if case is not None:
            attrs.update({"dx-case": case})
        if pattern is not None:
            attrs.update({"pattern": pattern})
        if autofocus:
            attrs.update({"autofocus": autofocus})
        if numeric:
            attrs.update({"dx-numeric": ""})
        if email:
            attrs.update(EMAIL_WIDGET_ATTRS)
        super().__init__(attrs=attrs)
