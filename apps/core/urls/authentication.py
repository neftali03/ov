from django.urls import path

from apps.core.views import authentication as vw

auth_patterns = [
    path("login/", vw.LoginView.as_view(), name="login"),
    path("logout/", vw.LogoutView.as_view(), name="logout"),
]
