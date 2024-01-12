from django.urls import path
from .views import (
    RegisterUser,
    LoginUser,
    UserView,
    LogoutUser,
    RefreshApi,
    SendAdvEmail,
)

urlpatterns = [
    path("register", RegisterUser.as_view(), name="register"),
    path("login", LoginUser.as_view(), name="login"),
    path("user", UserView.as_view(), name="user"),
    path("refresh", RefreshApi.as_view(), name="refresh"),
    path("logout", LogoutUser.as_view(), name="logout"),
    path("send-adv-email", SendAdvEmail.as_view(), name="send-adv-email"),
]
