from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any, Optional, Union

from django.conf import settings
from django.http import HttpRequest

from apps.core.models import User
from common.http import reverse
from common.templates import NO_RECORDS, NO_VALUE

MAIN_NAMESPACE = "core"


@dataclass
class SubMenu:
    """A sidebar submenu."""

    title: str
    view_name: str
    view_kwargs: dict[str, Any] = field(default_factory=dict)
    perms: Optional[Union[list[str], str]] = None
    perms_funcs: Optional[Union[list[Callable], Callable]] = None
    allowed: bool = False
    url: Optional[str] = None
    is_active: bool = False

    def __post_init__(self):
        """Extend to set permissions and submenus."""
        self.url = reverse(self.view_name, **self.view_kwargs)

    def check_perms(self, user: User) -> bool:
        """Return True if the user has access permission."""
        if not self.allowed and self.perms is not None:
            if isinstance(self.perms, list):
                for perm in self.perms:
                    self.allowed = user.has_perm(perm)
                    if self.allowed:
                        break
            else:
                self.allowed = user.has_perm(self.perms)

        if not self.allowed and self.perms_funcs is not None:
            if isinstance(self.perms_funcs, list):
                for func in self.perms_funcs:
                    self.allowed = func(user)
                    if self.allowed:
                        break
            else:
                self.allowed = self.perms_funcs(user)

        return self.allowed

    def check_is_active(self, namespace: str) -> None:
        """Set the sub-menu as active or not."""
        if namespace == MAIN_NAMESPACE:
            self.is_active = False
        else:
            namespace = ":".join(namespace.split(":")[:2])
            self.is_active = self.view_name.startswith(namespace)


@dataclass
class Menu:
    """A sidebar menu."""

    title: str
    request: HttpRequest
    submenus: list[SubMenu]
    allowed: bool = False
    is_active: bool = False
    exclude_viewnames: Optional[list[str]] = None

    def __post_init__(self):
        """Set permissions and submenus."""
        namespace = ":".join(self.request.resolver_match.namespaces)
        viewname = f"{namespace}:{self.request.resolver_match.url_name}"
        for submenu in self.submenus:
            # noinspection PyTypeChecker
            if submenu.check_perms(self.request.user):
                if not self.exclude_viewnames or viewname not in self.exclude_viewnames:
                    submenu.check_is_active(namespace)
            self.allowed = self.allowed or submenu.allowed
            self.is_active = self.is_active or submenu.is_active


def sidebar(request) -> dict:
    """Return sidebar categories."""
    return {
        "menus": [
            Menu(
                title="Orientación",
                request=request,
                submenus=[
                    # SubMenu(
                    #     title="Iniciar evaluación",
                    # perms="",
                    # view_name="vocacional:start",
                    # ),
                    SubMenu(
                        title="Preguntas",
                        perms="",
                        view_name="core:faq:faq",
                    ),
                ],
            ),
            Menu(
                title="Administración",
                request=request,
                submenus=[
                    #     SubMenu(
                    #         title="Accesos",
                    #         perms_funcs=user_is_management,
                    #         view_name="core:authorization:list_authorization",
                    #     ),
                    # SubMenu(
                    #     title="Roles",
                    #     perms="auth.view_group",
                    #     view_name="users:role:list",
                    # ),
                    # SubMenu(
                    #     title="Usuarios",
                    #     perms="users.view_user",
                    #     view_name="users:user:list",
                    # ),
                    # SubMenu(
                    #     title="Configuraciones",
                    #     perms="index.list_settings",
                    #     view_name="index:setting:list",
                    # ),
                    # SubMenu(
                    #     title="Peticiones",
                    #     perms="audit.view_request_log",
                    #     view_name="audit:requests:list",
                    # ),
                    # SubMenu(
                    #     title="Tareas",
                    #     perms="index.list_task",
                    #     view_name="index:tasks:list",
                    # ),
                ],
            ),
        ]
    }


# noinspection PyUnusedLocal
def custom_data(request):
    """Return a flag indicating if in debug mode or not."""
    return {
        "DEBUG": settings.DEBUG,
        "NO_VALUE": NO_VALUE,
        "NO_RECORDS": NO_RECORDS,
    }
