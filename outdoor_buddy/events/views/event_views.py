from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import modelform_factory
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from outdoor_buddy.events.models import Event
from outdoor_buddy.events.forms import EventForm
from outdoor_buddy.utils.views_mixins import UserIsOwnerMixin, ReadOnlyFormMixin
from services.s3 import S3Service


class EventDetailView(LoginRequiredMixin, DetailView):
    model = Event
    template_name = "events/event-detail.html"
    context_object_name = "event"

    def get_object(self, queryset=None):
        """
        Fetch the specific event based on its ID and ensure it exists.
        """
        return get_object_or_404(Event, pk=self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        """
        Add additional context data if necessary (e.g., related participants).
        """
        context = super().get_context_data(**kwargs)
        event = self.object
        context["organizer_profile"] = getattr(event.creator, "profile", None)  # Add organizer's profile
        return context


class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = "events/event-create.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class EventUpdateView(LoginRequiredMixin, UserIsOwnerMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = "events/event-edit.html"
    success_url = reverse_lazy("event-list")

    def get_object(self, queryset=None):
        """
        Fetch the specific event object being edited.
        """
        event = super().get_object(queryset)
        # Optionally: Add access control logic here if needed.
        return event

    def form_valid(self, form):
        """
        Handles form submission, including updating the event picture.
        """
        event = form.save(commit=False)

        # Handle picture upload
        if "picture_upload" in form.changed_data and event.picture_upload:
            s3_service = S3Service()  # Assume this handles S3 interactions
            old_picture_key = event.picture_upload.name
            try:
                s3_service.s3.delete_object(
                    Bucket=s3_service.bucket_name,
                    Key=old_picture_key,
                )
            except Exception as e:
                print(f"Error deleting file from S3: {e}")

        event.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """
        Provide additional context to the template.
        """
        context = super().get_context_data(**kwargs)
        context["event"] = self.get_object()
        return context

    def get_success_url(self):
        """
        Redirect to the event detail page after a successful update.
        """
        return reverse_lazy("event-detail", kwargs={"pk": self.object.pk})


class EventDeleteView(LoginRequiredMixin, ReadOnlyFormMixin, UserIsOwnerMixin, DeleteView):
    model = Event
    template_name = "events/event-delete.html"
    form_class = modelform_factory(
        Event,
        exclude=(
            ["id", "creator"]
        )
    )
    success_url = reverse_lazy('home')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["instance"] = self.object
        return kwargs

