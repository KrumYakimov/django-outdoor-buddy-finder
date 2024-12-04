from django.urls import path, include

from outdoor_buddy.events import views

urlpatterns = [
    path("my-events/", views.UserEventListView.as_view(), name="user-event-list"),
    path("create/", views.EventCreateView.as_view(), name="event-create"),
    path(
        "<int:pk>/",
        include(
            [
                path("details/", views.EventDetailView.as_view(), name="event-detail"),
                path("update/", views.EventUpdateView.as_view(), name="event-update"),
                path("delete/", views.EventDeleteView.as_view(), name="event-delete"),
            ]
        ),
    ),
    path(
        "<int:event_id>",
        include(
            [
                path("join/", views.JoinEventView.as_view(), name="join-event"),
                path("leave/", views.LeaveEventView.as_view(), name="leave-event"),
                path(
                    "join/done/",
                    views.JoinEventDoneView.as_view(),
                    name="join-event-done",
                ),
                path(
                    "leave/done/",
                    views.LeaveEventDoneView.as_view(),
                    name="leave-event-done",
                ),
            ]
        ),
    ),
    path("hiking/", views.HikingEventListView.as_view(), name="hiking-events"),
    path("skiing/", views.SkiingEventListView.as_view(), name="skiing-events"),
    path("kayaking/", views.KayakingEventListView.as_view(), name="kayaking-events"),
    path(
        "mountain-biking/",
        views.MountainBikingEventListView.as_view(),
        name="mountain-biking-events",
    ),
]
