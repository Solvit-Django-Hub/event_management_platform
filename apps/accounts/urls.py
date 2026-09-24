from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import RegisterView, LoginView, LogoutView,ProfileView, ChangePasswordView,ActivateAccountView,ForgotPasswordView,ResetPasswordView


urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    #path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/change-password/",ChangePasswordView.as_view(),name="change_password"),
    path("activate/",ActivateAccountView.as_view(),name="activate_account"),

    path("forgot-password/",ForgotPasswordView.as_view(),name="forgot_password"),

    path("reset-password/",ResetPasswordView.as_view(),name="reset_password",)
]


