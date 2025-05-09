from typing import Any, Dict, Optional

from django import template

from common.http import reverse

register = template.Library()


def _link(
    viewname: str,
    *view_args: Any,
    label: str,
    style: str = "primary",
    size: str = "sm",
    classes: Optional[str] = None,
    attrs: Optional[str] = None,
    icon: Optional[str] = None,
    query_string: Optional[str] = None,
) -> Dict[str, str]:
    """
    Return the data to render a button link.

    Only positional arguments are allowed to the view.
    """
    url = reverse(viewname, *view_args)
    return {
        "link_url": url,
        "link_label": label,
        "link_style": style,
        "link_size": size,
        "link_classes": f" {classes}" if classes else "",
        "link_attrs": f" {attrs}" if attrs else "",
        "link_icon": icon or "",
        "link_query_string": query_string or "",
    }


@register.inclusion_tag("common/_link.html")
def link(
    viewname: str,
    *view_args: Any,
    label: str,
    style: str = "primary",
    size: str = "sm",
    classes: Optional[str] = None,
    attrs: Optional[str] = None,
    icon: Optional[str] = None,
    query_string: Optional[str] = None,
    **query_kwargs: Dict[str, Any],
) -> Dict[str, str]:
    """Render a standard button link."""
    query_string = query_string or ""
    query_string += "&".join([f"{key}={value}" for key, value in query_kwargs.items()])
    return _link(
        viewname,
        *view_args,
        label=label,
        style=style,
        size=size,
        classes=classes,
        attrs=attrs,
        icon=icon,
        query_string=query_string,
    )


@register.inclusion_tag("common/_link.html")
def link_create(
    viewname: str,
    *view_args: Any,
    size: str = "sm",
    classes: Optional[str] = None,
    attrs: Optional[str] = None,
) -> Dict[str, str]:
    """Render a standard button link."""
    return _link(
        viewname,
        *view_args,
        label="Crear",
        style="success",
        size=size,
        classes=classes,
        attrs=attrs,
    )


@register.inclusion_tag("common/_link.html")
def link_cancel(
    viewname: str,
    *view_args: Any,
    size: str = "sm",
    classes: Optional[str] = None,
    attrs: Optional[str] = None,
) -> Dict[str, str]:
    """Render a standard button link."""
    return _link(
        viewname,
        *view_args,
        label="Cancelar",
        style="secondary",
        size=size,
        classes=classes,
        attrs=attrs,
    )


@register.inclusion_tag("common/_link.html")
def link_edit(
    viewname: str,
    *view_args: Any,
    size: str = "sm",
    classes: Optional[str] = None,
    attrs: Optional[str] = None,
) -> Dict[str, str]:
    """Render a standard button link."""
    return _link(
        viewname,
        *view_args,
        label="Actualizar",
        style="warning",
        size=size,
        classes=classes,
        attrs=attrs,
    )


@register.inclusion_tag("common/_link.html")
def link_delete(
    viewname: str,
    *view_args: Any,
    size: str = "sm",
    classes: Optional[str] = None,
    icon: Optional[str] = None,
    attrs: Optional[str] = None,
) -> Dict[str, str]:
    """Render a standard delete button link."""
    return _link(
        viewname,
        *view_args,
        label="Eliminar",
        style="danger",
        size=size,
        classes=classes,
        icon=icon,
        attrs=attrs,
    )
