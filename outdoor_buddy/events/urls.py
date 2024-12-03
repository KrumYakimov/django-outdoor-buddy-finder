from django.urls import path, include
from outdoor_buddy.events import views

urlpatterns = [
    # path("", views.EventListView.as_view(), name="event-list"),
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
]
