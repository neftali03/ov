from datetime import datetime
from typing import Any, Optional, Union

from django.core.validators import (MaxValueValidator, MinLengthValidator,
                                    MinValueValidator, RegexValidator)
from django.db import models
from django.utils.timezone import get_default_timezone

from common.dx_django_base.validators import NumericStringValidator

EMPTY_STRING = "--"
NULL_STRING = "Nulo"


# noinspection DuplicatedCode
class CharField(models.CharField):
    """Custom `CharField`."""

    audit_trail = True

    def __init__(
        self,
        *args,
        min_length=None,
        numeric_str=False,
        regex=None,
        db_collation=None,
        audit_trail=True,
        audit_callback=None,
        **kwargs,
    ):
        """Extend to include extra validations."""
        validators = kwargs.pop("validators", [])
        if min_length is not None:
            validators.append(MinLengthValidator(min_length))
        if numeric_str:
            validators.append(NumericStringValidator())
        if regex is not None:
            validators.append(RegexValidator(regex=regex))
        kwargs["validators"] = validators

        super().__init__(*args, db_collation=db_collation, **kwargs)
        self.audit_trail = audit_trail
        self.audit_callback = audit_callback

    def to_audit_trail(self, value: Optional[str]) -> Any:
        """Return a representation for the audit trail."""
        if self.audit_callback is not None:
            return self.audit_callback(value)
        if not value:
            return EMPTY_STRING
        return value


# noinspection DuplicatedCode
class PositiveSmallIntegerField(models.PositiveSmallIntegerField):
    """Custom `PositiveSmallIntegerField`."""

    def __init__(
        self,
        *args,
        audit_trail=True,
        audit_callback=None,
        **kwargs,
    ):
        """Extend to customize class."""
        super().__init__(*args, **kwargs)
        self.audit_trail = audit_trail
        self.audit_callback = audit_callback

    def to_audit_trail(self, value: Optional[int]) -> Any:
        """Return a representation for the audit trail."""
        if self.audit_callback is not None:
            return self.audit_callback(value)
        if value is None:
            return NULL_STRING
        if self.choices:
            for choice, label in self.choices:
                if value == choice:
                    return label
        return f"{value:,}"


# noinspection DuplicatedCode
class IntegerField(models.IntegerField):
    """Custom `IntegerField`."""

    def __init__(
        self,
        *args,
        min_value=None,
        max_value=None,
        audit_trail=True,
        audit_callback=None,
        **kwargs,
    ):
        """Extend to customize class."""
        validators = kwargs.pop("validators", [])
        if min_value is not None:
            validators.append(MinValueValidator(min_value))
        if max_value is not None:
            validators.append(MaxValueValidator(max_value))
        kwargs["validators"] = validators

        super().__init__(*args, **kwargs)
        self.audit_trail = audit_trail
        self.audit_callback = audit_callback

    def to_audit_trail(self, value: Optional[int]) -> Any:
        """Return a representation for the audit trail."""
        if self.audit_callback is not None:
            return self.audit_callback(value)
        if value is None:
            return NULL_STRING
        if self.choices:
            for choice, label in self.choices:
                if value == choice:
                    return label
        return f"{value:,}"


# noinspection DuplicatedCode
class BooleanField(models.BooleanField):
    """Custom `BooleanField`."""

    def __init__(
        self,
        *args,
        audit_trail=True,
        audit_callback=None,
        **kwargs,
    ):
        """Extend to customize class."""
        super().__init__(*args, **kwargs)
        self.audit_trail = audit_trail
        self.audit_callback = audit_callback

    def to_audit_trail(self, value: Union[bool, None]) -> Any:
        """Return a representation for the audit trail."""
        if self.audit_callback is not None:
            return self.audit_callback(value)
        if value is None:
            return NULL_STRING
        if self.choices:
            for choice, label in self.choices:
                if value == choice:
                    return label
        return "Sí" if value else "No"


# noinspection DuplicatedCode
class DateTimeField(models.DateTimeField):
    """Custom `DateTimeField`."""

    def __init__(
        self,
        *args,
        audit_trail=True,
        audit_callback=None,
        **kwargs,
    ):
        """Extend to customize class."""
        super().__init__(*args, **kwargs)
        self.audit_trail = audit_trail
        self.audit_callback = audit_callback

    def to_audit_trail(self, value: Optional[datetime]) -> Any:
        """Return a representation for the audit trail."""
        if self.audit_callback is not None:
            return self.audit_callback(value)
        if value is None:
            return NULL_STRING
        if self.choices:
            for choice, label in self.choices:
                if value == choice:
                    return label
        return value.astimezone(get_default_timezone()).strftime("%d/%m/%Y %H:%M:%S")


# noinspection DuplicatedCode
class ForeignKey(models.ForeignKey):
    """Custom `ForeignKey`."""

    def __init__(
        self,
        to,
        on_delete=models.PROTECT,
        related_name=None,
        related_query_name=None,
        limit_choices_to=None,
        parent_link=False,
        to_field=None,
        db_constraint=True,
        audit_trail=True,
        audit_callback=None,
        **kwargs,
    ):
        """Extend to include a default value for `on_dele` param."""
        super().__init__(
            to,
            on_delete,
            related_name=related_name,
            related_query_name=related_query_name,
            limit_choices_to=limit_choices_to,
            parent_link=parent_link,
            to_field=to_field,
            db_constraint=db_constraint,
            **kwargs,
        )
        self.audit_trail = audit_trail
        self.audit_callback = audit_callback

    def to_audit_trail(self, value) -> Any:
        """Return a representation for the audit trail."""
        if self.audit_callback is not None:
            return self.audit_callback(value)
        if value is None:
            return NULL_STRING
        if self.choices:
            for choice, label in self.choices:
                if value == choice:
                    return label
        return str(value)


# noinspection DuplicatedCode
class ManyToManyField(models.ManyToManyField):
    """Custom `ManyToManyField`."""

    def __init__(
        self,
        *args,
        audit_trail=True,
        **kwargs,
    ):
        """Extend to customize class."""
        super().__init__(*args, **kwargs)
        self.audit_trail = audit_trail


# noinspection DuplicatedCode
class TextField(models.TextField):
    """Custom `TextField`."""

    def __init__(
        self,
        *args,
        audit_trail=True,
        audit_callback=None,
        numeric_str=False,
        regex=None,
        **kwargs,
    ):
        """Extend to customize class."""
        validators = kwargs.pop("validators", [])
        if numeric_str:
            validators.append(NumericStringValidator())
        if regex is not None:
            validators.append(RegexValidator(regex=regex))
        kwargs["validators"] = validators

        super().__init__(*args, **kwargs)

        self.audit_trail = audit_trail
        self.audit_callback = audit_callback


# noinspection DuplicatedCode
class PositiveBigIntegerField(models.PositiveBigIntegerField):
    """Custom `PositiveBigIntegerField`."""

    def __init__(
        self,
        *args,
        audit_trail=True,
        audit_callback=None,
        **kwargs,
    ):
        """Extend to customize class."""
        super().__init__(*args, **kwargs)
        self.audit_trail = audit_trail
        self.audit_callback = audit_callback

    def to_audit_trail(self, value: Optional[int]) -> Any:
        """Return a representation for the audit trail."""
        if self.audit_callback is not None:
            return self.audit_callback(value)
        if value is None:
            return NULL_STRING
        if self.choices:
            for choice, label in self.choices:
                if value == choice:
                    return label
        return f"{value:,}"


# noinspection DuplicatedCode
class JSONField(models.JSONField):
    """Custom `JSONField`."""

    def __init__(
        self,
        *args,
        audit_trail=True,
        audit_callback=None,
        **kwargs,
    ):
        """Extend to customize class."""
        super().__init__(*args, **kwargs)
        self.audit_trail = audit_trail
        self.audit_callback = audit_callback

    def to_audit_trail(self, value: Union[list, dict, None]) -> Any:
        """Return a representation for the audit trail."""
        if self.audit_callback is not None:
            return self.audit_callback(value)
        if not value:
            return NULL_STRING
        if self.choices:
            for choice, label in self.choices:
                if value == choice:
                    return label
        return value
