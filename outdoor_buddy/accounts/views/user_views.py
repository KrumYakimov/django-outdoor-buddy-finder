import logging

from django.contrib.auth import get_user_model, login, views as auth_view
from django.db import transaction
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic as views

from outdoor_buddy.accounts.forms import AppUserCreationForm

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
