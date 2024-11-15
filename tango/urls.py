from django.contrib.auth.views import LogoutView
from django.urls import path

from tango.views import index, login_view, register_user

urlpatterns = [
    path("", index, name="index"),
    path("login/", login_view, name="login"),
    path("register/", register_user, name="register"),
    path("logout/", LogoutView.as_view(), name="logout")
]

app_name = "tango"