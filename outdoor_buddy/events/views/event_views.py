from collections import defaultdict

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg
from django.forms import modelform_factory
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from rest_framework import generics
from rest_framework.filters import SearchFilter, OrderingFilter

from outdoor_buddy.events.forms import EventForm
from outdoor_buddy.events.models import Event
from outdoor_buddy.events.serializers import EventSerializer
from outdoor_buddy.reviews.forms import ReviewForm
from outdoor_buddy.utils.views_mixins import UserIsOwnerMixin, ReadOnlyFormMixin
from services.s3 import S3Service

UserModel = get_user_model()


class EventListAPIView(generics.ListAPIView):
    """
    API endpoint to list all events.
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'location', 'activity_type__name']


class UserEventListView(LoginRequiredMixin, ListView):
    model = Event
    template_name = "events/user-events.html"
    context_object_name = "user_events"

    def get_queryset(self):
        """
        Fetch events created by the logged-in user with related activity types preloaded.
        """
        return (
            Event.objects.filter(creator=self.request.user)
            .select_related("activity_type")
            .order_by("start_datetime")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()

        grouped_events = defaultdict(list)
        for event in queryset:
            grouped_events[event.activity_type.name].append(event)

        context["user_events"] = dict(grouped_events)
        return context


class EventDetailView(LoginRequiredMixin, DetailView):
    model = Event
    template_name = "events/event-details.html"
    context_object_name = "event"

    def get_object(self, queryset=None):
        """
        Fetch the specific event based on its ID and ensure it exists.
        """
        return get_object_or_404(Event, pk=self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        """
        Add additional context data including organizer profile, activity type,
        return URL, reviews, and review-related information.
        """
        context = super().get_context_data(**kwargs)
        event = self.get_object()

        context.update(
            {
                "organizer_profile": getattr(event.creator, "profile", None),
                "activity_name": event.activity_type.name.lower().replace(" ", "-"),
                "return_url": self.get_return_url(),
            }
        )

        context["is_participant"] = event.participants.filter(
            user=self.request.user
        ).exists()

        reviews = event.reviews.select_related("reviewer__profile").all()
        average_rating = reviews.aggregate(Avg("rating"))["rating__avg"]

        user_review = reviews.filter(reviewer=self.request.user).first()

        context.update(
            {
                "reviews": reviews,
                "average_rating": average_rating or 0,
                "user_review": user_review,
                "review_form": ReviewForm(instance=user_review),
            }
        )

        return context

    def get_return_url(self):
        """
        Determine the return URL based on the referrer or fallback to the activity-specific or user-event list views.
        """
        referer = self.request.META.get("HTTP_REFERER")
        if referer:
            return referer  # Prioritize the referrer to return to where the user came from.

        activity_slug = self.object.activity_type.name.lower().replace(" ", "-")
        activity_urls = {
            "hiking": "hiking-events",
            "skiing": "skiing-events",
            "kayaking": "kayaking-events",
            "mountain-biking": "mountain-biking-events",
        }

        return reverse(activity_urls.get(activity_slug, "user-event-list"))

    def post(self, request, *args, **kwargs):
        """
        Handle review submission.
        """
        event = self.get_object()
        review_form = ReviewForm(request.POST)

        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.reviewer = request.user
            review.event = event
            review.save()
            return redirect("event-detail", pk=event.pk)

        return self.render_to_response(self.get_context_data(review_form=review_form))


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
        return event

    def form_valid(self, form):
        """
        Handles form submission, including updating the event picture.
        """
        event = form.save(commit=False)

        if "picture_upload" in form.changed_data and event.picture_upload:
            s3_service = S3Service()
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


class EventDeleteView(
    LoginRequiredMixin, ReadOnlyFormMixin, UserIsOwnerMixin, DeleteView
):
    model = Event
    template_name = "events/event-delete.html"
    form_class = modelform_factory(Event, exclude=(["id", "creator"]))
    success_url = reverse_lazy("home")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["instance"] = self.object
        return kwargs
