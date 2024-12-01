import logging

from django.contrib import messages
from django.contrib.auth import get_user_model, login, views as auth_view
from django.contrib.auth import mixins as auth_mixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.db import transaction
from django.forms import modelform_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_encode
from django.views import generic as views
from django.views.generic import UpdateView, TemplateView, DeleteView

from outdoor_buddy import settings
from outdoor_buddy.accounts.forms import AppUserCreationForm, AccountEmailChangeForm, ProfileForm, ContactForm
from outdoor_buddy.accounts.models import Profile, Contact
from outdoor_buddy.utils.mixins import ReadOnlyFormMixin
from services.s3 import S3Service

logger = logging.getLogger(__name__)

UserModel = get_user_model()


class SignupView(views.CreateView):
    model = UserModel
    form_class = AppUserCreationForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        try:
            with transaction.atomic():
                user = form.save()
                login(self.request, user)
                return HttpResponseRedirect(self.success_url)
        except Exception as e:
            logger.error(
                f"Error during registration for email {form.cleaned_data.get('email')}: {e}"
            )
            form.add_error(
                None,
                "An error occurred while processing your registration. Please try again.",
            )
            return self.form_invalid(form)


class SigninView(auth_view.LoginView):
    template_name = "accounts/signin.html"
    redirect_authenticated_user = True
    # authentication_form = CustomAuthenticationForm


class AccountPasswordChangeView(
    auth_mixin.LoginRequiredMixin, auth_view.PasswordChangeView
):
    template_name = "accounts/password-change.html"
    success_url = reverse_lazy("password-change-done")


class AccountResetPasswordView(auth_view.PasswordResetView):
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


class AccountPasswordResetDoneView(auth_view.PasswordResetDoneView):
    template_name = "accounts/password_reset_done.html"


class AccountPasswordResetConfirmView(auth_view.PasswordResetConfirmView):
    template_name = "accounts/password_reset_confirm.html"


class AccountPasswordResetCompleteView(auth_view.PasswordResetCompleteView):
    template_name = "accounts/password_reset_complete.html"


class AccountEmailChangeView(
    SuccessMessageMixin, auth_mixin.LoginRequiredMixin, views.UpdateView
):
    form_class = AccountEmailChangeForm
    template_name = "accounts/email-change.html"
    success_url = reverse_lazy("email-change-done")

    def get_object(self, queryset=None):
        return UserModel.objects.get(pk=self.request.user.pk)


class AccountEmailChangeDoneView(views.TemplateView):
    template_name = "accounts/email-change-done.html"


class ProfileContactView(auth_mixin.LoginRequiredMixin, TemplateView):
    template_name = "accounts/profile-view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context["profile"] = Profile.objects.get(user=user)
        context["contact"] = Contact.objects.get(user=user)

        return context


class ProfileContactUpdateView(auth_mixin.LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = 'accounts/profile-edit.html'
    form_class = ProfileForm

    def get_object(self, queryset=None):
        profile = self.request.user.profile
        print(f"Fetched Profile: {profile}")  # Debug log
        return profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add Contact form to the context
        context['contact_form'] = ContactForm(instance=self.request.user.contact)
        return context

    # def form_valid(self, form):
    #     profile = form.save(commit=False)
    #     print(f"Profile user before assignment: {profile.user}")  # Debug log
    #     if not profile.user:
    #         profile.user = self.request.user
    #     print(f"Profile user after assignment: {profile.user}")  # Debug log
    #     profile.save()
    #
    #     contact_form = ContactForm(self.request.POST, instance=self.request.user.contact)
    #     if contact_form.is_valid():
    #         contact_form.save()
    #     else:
    #         print("ContactForm errors:", contact_form.errors)
    #
    #     return super().form_valid(form)

    def form_valid(self, form):
        profile = form.save(commit=False)

        # Delete old profile picture if a new one is uploaded
        if 'picture_upload' in form.changed_data and profile.picture_upload:
            s3_service = S3Service()
            old_picture_key = profile.picture_upload.name
            try:
                s3_service.s3.delete_object(
                    Bucket=s3_service.bucket_name,
                    Key=old_picture_key,
                )
            except Exception as e:
                print(f"Error deleting file from S3: {e}")

        if not profile.user:
            profile.user = self.request.user

        profile.save()

        contact_form = ContactForm(self.request.POST, instance=self.request.user.contact)
        if contact_form.is_valid():
            contact_form.save()
        else:
            print("ContactForm errors:", contact_form.errors)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('profile')  # Redirect after successful edit


class UserDeleteView(auth_mixin.LoginRequiredMixin, ReadOnlyFormMixin, DeleteView):
    model = UserModel
    template_name = "accounts/profile-delete.html"
    success_url = reverse_lazy('home')  # Redirect to the home page after deletion

    def get_object(self, queryset=None):
        """
        Retrieve the User instance by primary key (pk) and include the related Profile and Contact.
        """
        app_user = get_object_or_404(UserModel, pk=self.kwargs['pk'])
        return app_user

    def get_context_data(self, **kwargs):
        """
        Add Profile and Contact forms with disabled fields to the context.
        """
        context = super().get_context_data(**kwargs)

        # Retrieve the related Profile and Contact instances
        profile = self.object.profile
        contact = self.object.contact

        # Create forms with disabled (readonly) fields
        ProfileForm = modelform_factory(Profile, exclude=['user'])
        ContactForm = modelform_factory(Contact, exclude=['user'])

        # Instantiate the forms with existing data
        context['profile_form'] = ProfileForm(instance=profile)
        context['contact_form'] = ContactForm(instance=contact)

        # Pass the actual profile and contact data separately for rendering
        context['profile'] = profile
        context['contact'] = contact

        return context

    def delete(self, request, *args, **kwargs):
        """
        Handle the deletion of Profile, Contact, and User.
        """
        app_user = self.get_object()

        # Delete the related Profile and Contact objects
        app_user.profile.delete()
        app_user.contact.delete()

        # Proceed with deleting the User
        return super().delete(request, *args, **kwargs)