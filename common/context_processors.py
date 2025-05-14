# from collections.abc import Callable
# from dataclasses import dataclass, field
# from typing import Any

from django.conf import settings

# from apps.core.models import User
# from common.http import reverse
# from common.permissions import user_is_api, user_is_management
from common.templates import NO_RECORDS, NO_VALUE

# from django.http import HttpRequest


MAIN_NAMESPACE = "core"


# @dataclass
# class SubMenu:
#     """A sidebar submenu."""
#
#     title: str
#     view_name: str
#     view_kwargs: dict[str, Any] = field(default_factory=dict)
#     perms: list[str] | str = None
#     perms_funcs: list[Callable] | Callable = None
#     allowed: bool = False
#     url: str = None
#     is_active: bool = False
#
#     def __post_init__(self):
#         """Extend to set permissions and submenus."""
#         self.url = reverse(self.view_name, **self.view_kwargs)
#
#     def check_perms(self, user: User) -> bool:
#         """Return True if the user has access permission."""
#         if not self.allowed and self.perms is not None:
#             if isinstance(self.perms, list):
#                 for perm in self.perms:
#                     self.allowed = user.has_perm(perm)
#                     if self.allowed:
#                         break
#             else:
#                 self.allowed = user.has_perm(self.perms)
#
#         if not self.allowed and self.perms_funcs is not None:
#             if isinstance(self.perms_funcs, list):
#                 for func in self.perms_funcs:
#                     self.allowed = func(user)
#                     if self.allowed:
#                         break
#             else:
#                 self.allowed = self.perms_funcs(user)
#
#         return self.allowed
#
#     def check_is_active(self, namespace: str) -> None:
#         """Set the sub-menu as active or not."""
#         if namespace == MAIN_NAMESPACE:
#             self.is_active = False
#         else:
#             namespace = ":".join(namespace.split(":")[:2])
#             self.is_active = self.view_name.startswith(namespace)
#
#
# @dataclass
# class Menu:
#     """A sidebar menu."""
#
#     title: str
#     request: HttpRequest
#     submenus: list[SubMenu]
#     allowed: bool = False
#     is_active: bool = False
#     exclude_viewnames: list[str] = None
#
#     def __post_init__(self):
#         """Set permissions and submenus."""
#         namespace = ":".join(self.request.resolver_match.namespaces)
#         viewname = f"{namespace}:
#         {self.request.resolver_match.url_name}"
#         for submenu in self.submenus:
#             # noinspection PyTypeChecker
#             if submenu.check_perms(self.request.user):
#                 if not self.exclude_viewnames or
#                 viewname not in self.exclude_viewnames:
#                     submenu.check_is_active(namespace)
#             self.allowed = self.allowed or submenu.allowed
#             self.is_active = self.is_active or submenu.is_active
#
#
# def sidebar(request) -> dict:
#     """Return sidebar categories."""
#     return {
#         "menus": [
#             Menu(
#                 title="Empresas",
#                 request=request,
#                 submenus=[
#                     SubMenu(
#                         title="Empresas",
#                         perms="companies.list_company",
#                         view_name="companies:company:list",
#                     ),
#                     SubMenu(
#                         title="Ubicaciones",
#                         perms="companies.list_location",
#                         view_name="companies:location:list",
#                     ),
#                     SubMenu(
#                         title="Cajas",
#                         perms="companies.list_point_of_sale",
#                         view_name="companies:point_of_sale:list",
#                     ),
#                 ],
#             ),
#             Menu(
#                 title="Clientes",
#                 request=request,
#                 submenus=[
#                     SubMenu(
#                         title="Clientes",
#                         perms="customers.list_customer",
#                         view_name="customers:customer:search",
#                     ),
#                 ],
#             ),
#             Menu(
#                 title="Acreedores",
#                 request=request,
#                 submenus=[
#                     SubMenu(
#                         title="Acreedores",
#                         perms="suppliers.list_supplier",
#                         view_name="suppliers:supplier:search",
#                     ),
#                 ],
#             ),
#             Menu(
#                 title="Logística",
#                 request=request,
#                 submenus=[
#                     SubMenu(
#                         title="Recepciones",
#                         perms="logistics.list_reception",
#                         view_name="logistics:reception:list",
#                     ),
#                     SubMenu(
#                         title="Despachos",
#                         perms="logistics.list_delivery",
#                         view_name="logistics:delivery:list",
#                     ),
#                 ],
#             ),
#             Menu(
#                 title="Facturación",
#                 request=request,
#                 submenus=[
#                     SubMenu(
#                         title="Documentos",
#                         perms=[
#                             "einvoice.list_issuing_fe",
#                             "einvoice.list_issuing_ccfe",
#                             "einvoice.list_issuing_fexe",
#                             "einvoice.list_issuing_fsee",
#                             "einvoice.list_issuing_nce",
#                             "einvoice.list_issuing_nde",
#                             "einvoice.list_issuing_nre",
#                             "einvoice.list_issuing_cre",
#                         ],
#                         view_name="einvoice:issuing:search",
#                     ),
#                     SubMenu(
#                         title="Invalidaciones",
#                         perms=["einvoice.list_invalidation"],
#                         view_name="einvoice:invalidation:search",
#                     ),
#                     SubMenu(
#                         title="Contingencias",
#                         perms=["einvoice.list_contingency"],
#                         view_name="einvoice:contingency:search",
#                     ),
#                     SubMenu(
#                         title="Gestión",
#                         perms=["einvoice.list_pos_validation"],
#                         view_name="einvoice:management:index",
#                     ),
#                 ],
#             ),
#             Menu(
#                 title="DataX",
#                 request=request,
#                 submenus=[
#                     SubMenu(
#                         title="ITMA",
#                         perms=["datax.view_itma_sales_by_location"],
#                         view_name="datax:itma:index",
#                     ),
#                 ],
#             ),
#             Menu(
#                 title="Tiendas",
#                 request=request,
#                 submenus=[
#                     SubMenu(
#                         title="Cuadre de caja",
#                         perms=["stores.list_cash_balance_report"],
#                         view_name="stores:cash_balance_report:search",
#                     ),
#                 ],
#             ),
#             Menu(
#                 title="Administración",
#                 request=request,
#                 submenus=[
#                     SubMenu(
#                         title="Accesos",
#                         perms_funcs=user_is_management,
#                         view_name="core:authorization:list_authorization",
#                     ),
#                     # SubMenu(
#                     #     title="Roles",
#                     #     perms="auth.view_group",
#                     #     view_name="users:role:list",
#                     # ),
#                     # SubMenu(
#                     #     title="Usuarios",
#                     #     perms="users.view_user",
#                     #     view_name="users:user:list",
#                     # ),
#                     # SubMenu(
#                     #     title="Configuraciones",
#                     #     perms="index.list_settings",
#                     #     view_name="index:setting:list",
#                     # ),
#                     # SubMenu(
#                     #     title="Peticiones",
#                     #     perms="audit.view_request_log",
#                     #     view_name="audit:requests:list",
#                     # ),
#                     # SubMenu(
#                     #     title="Tareas",
#                     #     perms="index.list_task",
#                     #     view_name="index:tasks:list",
#                     # ),
#                     SubMenu(
#                         title="Especificaciones API",
#                         perms_funcs=user_is_api,
#                         view_name="apis:specs",
#                     ),
#                 ],
#                 # exclude_viewnames=
#                 ["core:authorization:list_authorization"],
#             ),
#         ]
#     }


# noinspection PyUnusedLocal
def custom_data(request):
    """Return a flag indicating if in debug mode or not."""
    return {
        "DEBUG": settings.DEBUG,
        "NO_VALUE": NO_VALUE,
        "NO_RECORDS": NO_RECORDS,
    }
