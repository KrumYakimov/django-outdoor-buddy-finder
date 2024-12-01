import logging

from django.contrib.auth import get_user_model
from django.contrib.auth import mixins as auth_mixin
from django.forms import modelform_factory
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import UpdateView, TemplateView, DeleteView

from outdoor_buddy.accounts.forms import ProfileForm, ContactForm
from outdoor_buddy.accounts.models import Profile, Contact
from outdoor_buddy.utils.mixins import ReadOnlyFormMixin
from services.s3 import S3Service

logger = logging.getLogger(__name__)

UserModel = get_user_model()


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