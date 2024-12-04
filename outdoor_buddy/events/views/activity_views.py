from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView

from outdoor_buddy.events.models import Event, Activity


class HikingEventListView(ListView):
    model = Event
    template_name = "events/hiking-events.html"
    context_object_name = "hiking_events"

    def get_queryset(self):
        """
        Filter events based on activity type 'Hiking'.
        Assumes there's an Activity instance with the name 'Hiking'.
        """
        try:
            hiking_activity = Activity.objects.get(name="Hiking")
        except ObjectDoesNotExist:
            return Event.objects.none()
        return Event.objects.filter(activity_type=hiking_activity).order_by("start_datetime")


class SkiingEventListView(ListView):
    model = Event
    template_name = "events/skiing-events.html"
    context_object_name = "skiing_events"

    def get_queryset(self):
        """
        Filter events based on activity type 'Skiing'.
        Assumes there's an Activity instance with the name 'Skiing'.
        """
        try:
            skiing_activity = Activity.objects.get(name="Skiing")
        except ObjectDoesNotExist:
            return Event.objects.none()
        return Event.objects.filter(activity_type=skiing_activity).order_by("start_datetime")


class KayakingEventListView(ListView):
    model = Event
    template_name = "events/kayaking-events.html"
    context_object_name = "kayaking_events"

    def get_queryset(self):
        """
        Filter events based on activity type 'Kayaking'.
        Assumes there's an Activity instance with the name 'Kayaking'.
        """
        try:
            kayaking_activity = Activity.objects.get(name="Kayaking")
        except ObjectDoesNotExist:
            return Event.objects.none()
        return Event.objects.filter(activity_type=kayaking_activity).order_by("start_datetime")


class MountainBikingEventListView(ListView):
    model = Event
    template_name = "events/mountain-biking-events.html"  # Template for Mountain Biking
    context_object_name = "biking_events"

    def get_queryset(self):
        """
        Filter events based on activity type 'Mountain Biking'.
        Assumes there's an Activity instance with the name 'Mountain Biking'.
        """
        try:
            biking_activity = Activity.objects.get(name="Mountain Biking")
        except ObjectDoesNotExist:
            return Event.objects.none()
        return Event.objects.filter(activity_type=biking_activity).order_by("start_datetime")
