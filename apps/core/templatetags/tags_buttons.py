from typing import Optional

from django import template

register = template.Library()


def _button(
    label: str,
    style: str = "primary",
    size: str = "sm",
    classes: Optional[str] = None,
    attrs: Optional[str] = None,
    type_: str = "button",
) -> dict[str, str]:
    """Return the data to render a button."""
    return {
        "btn_label": label,
        "btn_style": style,
        "btn_size": size,
        "btn_classes": f" {classes}" if classes else "",
        "btn_attrs": f" {attrs}" if attrs else "",
        "btn_type": type_,
    }


@register.inclusion_tag("common/_button.html")
def button(
    label: str,
    *,
    style: str = "primary",
    size: str = "sm",
    classes: Optional[str] = None,
    attrs: Optional[str] = None,
) -> dict[str, str]:
    """Render a standard button."""
    return _button(label, style, size, classes, attrs)


@register.inclusion_tag("common/_button.html")
def button_cancel(
    *,
    size: str = "sm",
    classes: Optional[str] = None,
    attrs: Optional[str] = None,
) -> dict[str, str]:
    """Render a standard cancel button."""
    return _button("Cancelar", "secondary", size, classes, attrs)


@register.inclusion_tag("common/_button.html")
def button_delete(
    *,
    size: str = "sm",
    classes: Optional[str] = None,
    attrs: Optional[str] = None,
) -> dict[str, str]:
    """Render a standard delete button."""
    return _button("Eliminar", "danger", size, classes, attrs)


@register.inclusion_tag("common/_button.html")
def submit(
    label: str,
    *,
    style: str = "primary",
    size: str = "sm",
    classes: Optional[str] = None,
    attrs: Optional[str] = None,
) -> dict[str, str]:
    """Render a standard submit button."""
    return _button(label, style, size, classes, attrs, "submit")


@register.inclusion_tag("common/_button.html")
def submit_create(
    *,
    size: str = "sm",
    classes: Optional[str] = None,
    attrs: Optional[str] = None,
) -> dict[str, str]:
    """Render a standard submit create button."""
    return _button("Crear", "success", size, classes, attrs, "submit")


@register.inclusion_tag("common/_button.html")
def submit_add(
    *,
    size: str = "sm",
    classes: Optional[str] = None,
    attrs: Optional[str] = None,
) -> dict[str, str]:
    """Render a standard submit create button."""
    return _button("Agregar", "success", size, classes, attrs, "submit")


@register.inclusion_tag("common/_button.html")
def submit_edit(
    *,
    size: str = "sm",
    classes: Optional[str] = None,
    attrs: Optional[str] = None,
) -> dict[str, str]:
    """Render a standard submit edit button."""
    return _button("Actualizar", "warning", size, classes, attrs, "submit")


@register.inclusion_tag("common/_button.html")
def submit_delete(
    *,
    size: str = "sm",
    classes: Optional[str] = None,
    attrs: Optional[str] = None,
) -> dict[str, str]:
    """Render a standard submit delete button."""
    return _button("Eliminar", "danger", size, classes, attrs, "submit")


@register.inclusion_tag("common/_button.html")
def submit_start(
    *,
    size: str = "sm",
    classes: Optional[str] = None,
    attrs: Optional[str] = None,
) -> dict[str, str]:
    """Render a standard submit start button."""
    return _button("Iniciar", "primary", size, classes, attrs, "submit")


@register.inclusion_tag("common/_button.html")
def submit_cancel(
    *,
    size: str = "sm",
    classes: Optional[str] = None,
    attrs: Optional[str] = None,
) -> dict[str, str]:
    """Render a standard submit cancel button."""
    return _button("Anular", "secondary", size, classes, attrs, "submit")


@register.inclusion_tag("common/_button.html")
def submit_close(
    *,
    size: str = "sm",
    classes: Optional[str] = None,
    attrs: Optional[str] = None,
) -> dict[str, str]:
    """Render a standard submit close button."""
    return _button("Cerrar", "dark", size, classes, attrs, "submit")
