from django.urls import path

from outdoor_buddy.connections import views

urlpatterns = [
    path(
        "send/<int:user_id>/",
        views.SendBuddyRequestView.as_view(),
        name="send-buddy-request",
    ),
    path(
        "respond/<int:request_id>/",
        views.RespondBuddyRequestView.as_view(),
        name="respond-buddy-request",
    ),
    path(
        "disconnect/<int:user_id>/",
        views.DisconnectBuddyView.as_view(),
        name="disconnect-buddy",
    ),
    path("request-sent/", views.request_sent_view, name="request-sent"),
    path("request-accepted/", views.request_accepted_view, name="request-accepted"),
    path("request-declined/", views.request_declined_view, name="request-declined"),
    path(
        "disconnect-success/", views.disconnect_success_view, name="disconnect-success"
    ),
    path(
        "connected-profiles/",
        views.ConnectedProfilesView.as_view(),
        name="connected-profiles",
    ),
]
