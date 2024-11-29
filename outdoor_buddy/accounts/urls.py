from django.contrib.auth import views as auth_view
from django.urls import path
from outdoor_buddy.accounts import views

urlpatterns = [
    path("signup/", views.SignupView.as_view(), name="signup"),
    path("signin/", views.SigninView.as_view(), name="signin"),
    path("signout", auth_view.LogoutView.as_view(), name="signout"),
    path(
        "password-change/",
        views.AccountPasswordChangeView.as_view(
            template_name="accounts/password-change.html"
        ),
        name="password_change",
    ),
    path(
        "password-change-done/",
        auth_view.PasswordChangeDoneView.as_view(
            template_name="accounts/password-change-done.html"
        ),
        name="password-change-done",
    ),
    path(
        "reset-password/",
        views.AccountResetPasswordView.as_view(),
        name="reset_password",
    ),
    path(
        "reset-password/done/",
        views.AccountPasswordResetDoneView.as_view(),
        name="reset-password-done",
    ),
    path(
        "reset-password/confirm/<uidb64>/<token>/",
        views.AccountPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset-password/complete/",
        views.AccountPasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    path("email-change/", views.AccountEmailChangeView.as_view(), name="email-change"),
    path(
        "email-change/done/",
        views.AccountEmailChangeDoneView.as_view(),
        name="email-change-done",
    ),
]
