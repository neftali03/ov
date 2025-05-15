from django.urls import include, path

from apps.core.urls.authentication import auth_patterns
from apps.core.urls.frequently_asked_questions import faq_patterns
from apps.core.urls.user import user_patterns
from apps.core.views import index as vw

app_name = "core"

# noinspection PyUnresolvedReferences
urlpatterns = [
    path("", vw.index, name="index"),
    path("auth/", include((auth_patterns, app_name), namespace="auth")),
    path("user/", include((user_patterns, app_name), namespace="user")),
    path("faq/", include((faq_patterns, app_name), namespace="faq")),
]
