from django.urls import path, include
from accounts.views import register_user, login_user, logout_user, get_tokens_for_user

urlpatterns = [
    path("register/", register_user, name="register_user"),
    path("login/", login_user, name="login_user"),
    path("logout/", logout_user, name="logout_user"),
]
