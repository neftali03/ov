from django.db import models


def list_default():
    """Return an empty list for json/array."""
    return []


class NotEqual(models.Lookup):
    """A `not equal` query lookup."""

    lookup_name = "ne"

    def as_sql(self, compiler, connection):
        """Return SQL representation."""
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        params = lhs_params + rhs_params
        return f"{lhs} <> {rhs}", params


class TextChoices(models.TextChoices):
    """Custom text choices."""

    @classmethod
    def choices_dict(cls):
        """Return the choices/labels as a dictionary."""
        return dict(cls.choices)
