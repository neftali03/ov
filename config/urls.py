from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path("", include("apps.core.urls")),
    path("admin/", admin.site.urls),
    path(
        "favicon.ico/",
        RedirectView.as_view(url="/static/favicon.ico", permanent=True),
    ),
]


if settings.DEBUG:
    import debug_toolbar

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
