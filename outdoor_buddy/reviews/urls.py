from django.urls import path
from outdoor_buddy.reviews import views

urlpatterns = [
    path(
        "event/<int:pk>/review/",
        views.SubmitEventReviewView.as_view(),
        name="submit-event-review",
    ),
    path(
        "profile/<int:pk>/review/",
        views.SubmitProfileReviewView.as_view(),
        name="submit-profile-review",
    ),
]
