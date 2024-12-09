from datetime import timedelta
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now

from outdoor_buddy.events.models import Event, Activity
from outdoor_buddy.reviews.models import Review

UserModel = get_user_model()


class SubmitEventReviewViewTestCase(TestCase):
    @patch("outdoor_buddy.accounts.signals.send_welcome_email_to_user")
    def setUp(self, mock_send_email):
        mock_send_email.return_value = None
        self.user = UserModel.objects.create_user(
            email="reviewer@example.com", password="password"
        )
        self.activity = Activity.objects.create(name="Hiking")
        self.event = Event.objects.create(
            name="Test Event",
            start_datetime=now(),
            end_datetime=now() + timedelta(hours=3),
            location="Test Location",
            capacity=10,
            activity_type=self.activity,
            creator=self.user,
        )
        self.url = reverse("submit-event-review", kwargs={"pk": self.event.id})

    def test_valid_review_submission_creates_review(self):
        self.client.login(email="reviewer@example.com", password="password")
        response = self.client.post(self.url, {"rating": 5, "comment": "Great event!"})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Review.objects.filter(
                reviewer=self.user, event=self.event, rating=5, comment="Great event!"
            ).exists()
        )

    def test_update_existing_review(self):
        Review.objects.create(
            reviewer=self.user, event=self.event, rating=4, comment="Good event"
        )
        self.client.login(email="reviewer@example.com", password="password")
        response = self.client.post(self.url, {"rating": 5, "comment": "Great event!"})
        self.assertEqual(response.status_code, 302)
        review = Review.objects.get(reviewer=self.user, event=self.event)
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.comment, "Great event!")

    def test_invalid_rating_submission(self):
        self.client.login(email="reviewer@example.com", password="password")
        response = self.client.post(
            self.url, {"rating": 6, "comment": "Invalid rating"}
        )
        self.assertRedirects(
            response, reverse("event-detail", kwargs={"pk": self.event.id})
        )
        messages = list(response.wsgi_request._messages)
        self.assertIn(
            "Invalid rating. Please provide a rating between 1 and 5.",
            [m.message for m in messages],
        )
