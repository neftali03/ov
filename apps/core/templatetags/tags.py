from dataclasses import dataclass
from typing import Union

from django import template
from django.apps import apps

register = template.Library()


@dataclass
class BreadCrumb:
    """An item from a HTML breadcrumb element."""

    title: str
    url: Union[str, None] = None


@register.inclusion_tag("common/_breadcrumb.html", takes_context=True)
def breadcrumb(context) -> dict[str, Union[list[BreadCrumb], str]]:
    """
    Render the breadcrumb component.

    By default, the page title is added as the last/current item.
    """
    app_name = ""
    namespace = context["request"].resolver_match.namespaces
    joined_namespace = ":".join(namespace)

    if joined_namespace != "core":
        app_name = str(apps.get_app_config(namespace[0]).verbose_name)

    items = context.get("breadcrumbs", None)
    if isinstance(items, BreadCrumb):
        items = [items]

    page_title = context.get("page_title", "")
    return {"first_item": app_name, "items": items, "last_item": page_title}


@register.inclusion_tag("common/_page_subtitle.html")
def subtitle(content: str) -> dict[str, str]:
    """Render a page subtitle."""
    return {"subtitle": content}


@register.inclusion_tag("common/icons/_icon.html")
def icon(name: str) -> dict[str, str]:
    """Render an icon."""
    return {"icon_path": f"common/icons/_{name}.svg"}
