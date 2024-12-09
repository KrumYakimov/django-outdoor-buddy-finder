from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.utils.timezone import now
from django.views import View
from django.views.generic import TemplateView

from outdoor_buddy.events.models import Event, EventParticipant


class JoinEventView(LoginRequiredMixin, View):
    """
    Handles the functionality for users to join an event.
    """

    def post(self, request, *args, **kwargs):
        event_id = self.kwargs.get("event_id")
        redirect_to = request.POST.get("redirect_to", None)
        event = get_object_or_404(Event, id=event_id)

        if EventParticipant.objects.filter(user=request.user, event=event).exists():
            messages.warning(request, "You have already joined this event.")
            return redirect("event-detail", pk=event.id)

        if event.spots_remaining is not None and event.spots_remaining <= 0:
            messages.error(request, "This event is fully booked.")
            return redirect("event-detail", pk=event.id)

        if event.registration_deadline and now() > event.registration_deadline:
            messages.error(request, "Registration for this event has closed.")
            return redirect("event-detail", pk=event.id)

        EventParticipant.objects.create(user=request.user, event=event)

        return redirect("join-event-done", event_id=event.id)


class JoinEventDoneView(TemplateView):
    template_name = "events/join-event-done.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event_id = self.kwargs.get("event_id")
        event = get_object_or_404(Event, id=event_id)
        context["event"] = event
        return context


class LeaveEventView(LoginRequiredMixin, View):
    """
    Handles the functionality for users to leave an event.
    """

    def post(self, request, *args, **kwargs):
        event_id = self.kwargs.get("event_id")
        event = get_object_or_404(Event, id=event_id)

        participant = EventParticipant.objects.filter(user=request.user, event=event).first()
        if not participant:
            messages.warning(request, "You are not a participant in this event.")
            return redirect("event-detail", pk=event.id)

        participant.delete()

        return redirect("leave-event-done", event_id=event.id)


class LeaveEventDoneView(TemplateView):
    template_name = "events/leave-event-done.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event_id = self.kwargs.get("event_id")
        event = get_object_or_404(Event, id=event_id)
        context["event"] = event
        return context
