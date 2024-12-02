from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import (
    PasswordChangeView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_encode
from django.views.generic import UpdateView, TemplateView

from outdoor_buddy import settings
from outdoor_buddy.accounts.forms import AccountEmailChangeForm
from outdoor_buddy.utils.mixins import UserIsOwnerMixin

UserModel = get_user_model()


class AccountPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = "accounts/password-change.html"
    success_url = reverse_lazy("password-change-done")


class AccountResetPasswordView(PasswordResetView):
    template_name = "accounts/password_reset.html"
    success_url = reverse_lazy("reset-password-done")

    def send_mail(self, subject, message, from_email, recipient_list):
        """
        Override the send_mail method to send password reset email via SMTP.
        """
        user_email = recipient_list[0]
        token = default_token_generator.make_token(user_email)
        uid = urlsafe_base64_encode(user_email.encode())
        reset_link = self.request.build_absolute_uri(
            reverse_lazy(
                "password_reset_confirm", kwargs={"uidb64": uid, "token": token}
            )
        )

        subject = "Password Reset Request"
        html_content = render_to_string(
            "accounts/password_reset.html", {"reset_link": reset_link}
        )
        plain_text = (
            f"Please reset your password using the following link: {reset_link}"
        )

        send_mail(
            subject,
            plain_text,
            settings.EMAIL_HOST_USER,
            [user_email],
            html_message=html_content,
        )
        logger.info(f"Password reset email sent to {user_email}")


class AccountPasswordResetDoneView(PasswordResetDoneView):
    template_name = "accounts/password_reset_done.html"


class AccountPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "accounts/password_reset_confirm.html"


class AccountPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "accounts/password_reset_complete.html"


class AccountEmailChangeView(LoginRequiredMixin, UserIsOwnerMixin, UpdateView):
    form_class = AccountEmailChangeForm
    template_name = "accounts/email-change.html"
    success_url = reverse_lazy("email-change-done")

    def get_object(self, queryset=None):
        return UserModel.objects.get(pk=self.request.user.pk)


class AccountEmailChangeDoneView(TemplateView):
    template_name = "accounts/email-change-done.html"
