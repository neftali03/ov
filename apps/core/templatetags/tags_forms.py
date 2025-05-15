from django import template
from django.forms import Form

register = template.Library()


@register.inclusion_tag("common/forms/_non_field_errors.html")
def non_field_errors(form: Form) -> dict[str, Form]:
    """Render a standard form's non-fields-errors list."""
    return {"form": form}


@register.inclusion_tag("common/_page_subtitle.html")
def fieldset_subtitle(content: str) -> dict[str, str]:
    """Render a page subtitle."""
    return {"subtitle": content}
