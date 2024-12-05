from django.urls import path
from outdoor_buddy.reviews import views

urlpatterns = [
    path("event/<int:pk>/review/", views.SubmitReviewView.as_view(), name="submit-event-review"),
]
