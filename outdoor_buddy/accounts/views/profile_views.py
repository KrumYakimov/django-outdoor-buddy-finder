from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.forms import modelform_factory
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import UpdateView, TemplateView, DeleteView, ListView

from outdoor_buddy.accounts.forms import ProfileForm, ContactForm
from outdoor_buddy.accounts.models import Profile, Contact
from outdoor_buddy.connections.choices import StatusChoices
from outdoor_buddy.connections.models import BuddyRequest, Connection
from outdoor_buddy.utils.views_mixins import ReadOnlyFormMixin, UserIsOwnerMixin
from services.s3 import S3Service

UserModel = get_user_model()


class ExploreProfilesView(ListView):
    model = Profile
    template_name = "accounts/explore-profiles.html"
    context_object_name = "profiles"
    paginate_by = 6

    def get_queryset(self):
        # Fetch all profiles excluding superuser and staff users
        return Profile.objects.exclude(user__is_superuser=True).exclude(user__is_staff=True).select_related("user")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add current user's profile and contact explicitly
        if self.request.user.is_authenticated:
            context["my_profile"] = Profile.objects.get(user=self.request.user)
            context["my_contact"] = Contact.objects.get(user=self.request.user)

        return context


# class ProfileContactView(LoginRequiredMixin, TemplateView):
#     template_name = "accounts/profile-view.html"
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#
#         # Get the user_id from the URL kwargs
#         pk = self.kwargs.get("pk")
#
#         # Fetch the specified user
#         user = get_object_or_404(UserModel, id=pk)
#
#         # Exclude superuser and staff
#         if user.is_superuser or user.is_staff:
#             context["profile"] = None
#             context["contact"] = None
#         else:
#             # Fetch the associated Profile and Contact
#             context["profile"] = get_object_or_404(Profile, user=user)
#             context["contact"] = get_object_or_404(Contact, user=user)
#
#         return context


class ProfileContactView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/profile-view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pk = self.kwargs.get("pk")

        user = get_object_or_404(UserModel, id=pk)
        logged_in_user = self.request.user

        print(f"Debug: Profile user ID: {pk}, Logged-in user ID: {logged_in_user.id}")

        profile = get_object_or_404(Profile, user=user)
        contact = get_object_or_404(Contact, user=user)

        context.update({
            "profile": profile,
            "contact": contact,
            "is_buddy": False,
            "sent_request": None,
            "received_request": None,
        })

        if logged_in_user == user:
            # print("Debug: Logged-in user is viewing their own profile.")
            received_request = BuddyRequest.objects.filter(
                from_user__in=UserModel.objects.all(),
                to_user=logged_in_user,
                status=StatusChoices.PENDING
            ).first()

            context["received_request"] = received_request
            print(f"Received Request: {received_request}")
        else:

            buddy_status = Connection.objects.filter(
                Q(user1=logged_in_user, user2=user) |
                Q(user1=user, user2=logged_in_user)
            ).exists()

            sent_request = BuddyRequest.objects.filter(
                from_user=logged_in_user, to_user=user, status=StatusChoices.PENDING
            ).first()

            received_request = BuddyRequest.objects.filter(
                from_user=user, to_user=logged_in_user, status=StatusChoices.PENDING
            ).first()

            context.update({
                "is_buddy": buddy_status,
                "sent_request": sent_request,
                "received_request": received_request,
            })

        # print(f"Final Context: {context}")
        return context


class ProfileContactUpdateView(LoginRequiredMixin, UserIsOwnerMixin, UpdateView):
    model = Profile
    template_name = "accounts/profile-edit.html"
    form_class = ProfileForm

    def get_object(self, queryset=None):
        profile = self.request.user.profile
        # print(f"Fetched Profile: {profile}")  # Debug log
        return profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["contact_form"] = ContactForm(instance=self.request.user.contact)
        return context

    def form_valid(self, form):
        profile = form.save(commit=False)

        if "picture_upload" in form.changed_data and profile.picture_upload:
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

        contact_form = ContactForm(
            self.request.POST, instance=self.request.user.contact
        )
        if contact_form.is_valid():
            contact_form.save()
        else:
            print("ContactForm errors:", contact_form.errors)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("profile", kwargs={"pk": self.object.pk})


class UserDeleteView(LoginRequiredMixin, UserIsOwnerMixin, ReadOnlyFormMixin, DeleteView):
    model = UserModel
    template_name = "accounts/profile-delete.html"
    success_url = reverse_lazy("home")

    def get_object(self, queryset=None):
        """
        Retrieve the User instance by primary key (pk) and include the related Profile and Contact.
        """
        app_user = get_object_or_404(UserModel, pk=self.kwargs["pk"])
        return app_user

    def get_context_data(self, **kwargs):
        """
        Add Profile and Contact forms with disabled fields to the context.
        """
        context = super().get_context_data(**kwargs)

        profile = self.object.profile
        contact = self.object.contact

        ProfileForm = modelform_factory(Profile, exclude=["user"])
        ContactForm = modelform_factory(Contact, exclude=["user"])

        context["profile_form"] = ProfileForm(instance=profile)
        context["contact_form"] = ContactForm(instance=contact)

        context["profile"] = profile
        context["contact"] = contact

        return context

    def delete(self, request, *args, **kwargs):
        """
        Handle the deletion of Profile, Contact, and User.
        """
        app_user = self.get_object()

        app_user.profile.delete()
        app_user.contact.delete()

        return super().delete(request, *args, **kwargs)

