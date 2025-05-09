from typing import Optional

from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


class NumericStringValidator(RegexValidator):
    """Numeric string validator."""

    code = "numeric_str"
    message = _("Value must be numeric.")

    def __init__(self, message: Optional[str] = None):
        """Set numeric string regex."""
        super().__init__(regex="[^0-9]+", inverse_match=True, message=message)
