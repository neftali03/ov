from django.urls import path

from apps.core.views import user as vw

user_patterns = [
    path("password/change/", vw.change_password, name="change_password"),
]
