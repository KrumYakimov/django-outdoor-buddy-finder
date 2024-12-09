from datetime import timedelta
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase, Client
from django.urls import reverse
from django.utils.timezone import now

from outdoor_buddy.events.models import Activity, Event, EventParticipant

UserModel = get_user_model()


class EventListAPITestCase(TestCase):
    @patch("outdoor_buddy.accounts.signals.send_welcome_email")
    def setUp(self, mock_send_email):
        mock_send_email.return_value = None
        self.client = Client()
        self.user = UserModel.objects.create_user(email="testuser@example.com", password="password")
        self.activity = Activity.objects.create(name="Hiking")
        self.event = Event.objects.create(
            name="Test Event",
            start_datetime=now(),
            end_datetime=now() + timedelta(hours=2),
            location="Test Location",
            capacity=20,
            activity_type=self.activity,
            creator=self.user,
        )
        self.url = reverse("event-list")


class EventDetailViewTestCase(TestCase):
    @patch("outdoor_buddy.accounts.signals.send_welcome_email_to_user")
    def setUp(self, mock_send_email):
        mock_send_email.return_value = None
        self.client = Client()

        self.user = UserModel.objects.create_user(email="testuser@example.com", password="password")

        self.activity = Activity.objects.create(name="Hiking")
        self.event = Event.objects.create(
            name="Test Event",
            start_datetime=now(),
            end_datetime=now() + timedelta(hours=2),
            location="Test Location",
            capacity=20,
            activity_type=self.activity,
            creator=self.user,
        )

        self.url = reverse("event-detail", kwargs={"pk": self.event.pk})

    @patch("outdoor_buddy.accounts.signals.send_welcome_email_to_user")
    def test_event_detail_view(self, mock_send_email):
        mock_send_email.return_value = None

        self.client.login(email="testuser@example.com", password="password")
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Event")


class JoinEventTestCase(TestCase):
    @patch("outdoor_buddy.accounts.signals.send_welcome_email_to_user")
    def setUp(self, mock_send_email):
        mock_send_email.return_value = None
        self.client = Client()
        self.user = UserModel.objects.create_user(email="participant@example.com", password="password")
        self.activity = Activity.objects.create(name="Hiking")
        self.event = Event.objects.create(
            name="Joinable Event",
            start_datetime=now(),
            end_datetime=now() + timedelta(hours=3),
            location="Test Location",
            capacity=10,
            activity_type=self.activity,
            creator=self.user,
        )
        self.url = reverse("join-event", kwargs={"event_id": self.event.id})

    def test_join_event(self):
        self.client.login(email="participant@example.com", password="password")
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(EventParticipant.objects.filter(user=self.user, event=self.event).exists())


class UpdateEventTestCase(TestCase):
    @patch("outdoor_buddy.accounts.signals.send_welcome_email_to_user")
    def setUp(self, mock_send_email):
        mock_send_email.return_value = None
        self.user = UserModel.objects.create_user(email="creator@example.com", password="password")
        self.activity = Activity.objects.create(name="Hiking")
        self.event = Event.objects.create(
            name="Original Event",
            start_datetime=now(),
            end_datetime=now() + timedelta(hours=2),
            location="Original Location",
            capacity=20,
            activity_type=self.activity,
            creator=self.user,
            description="This is a test event.",
            registration_status="Open",
        )
        self.url = reverse("event-update", kwargs={"pk": self.event.pk})

    @patch("outdoor_buddy.accounts.signals.send_welcome_email_to_user")
    def test_update_event(self, mock_send_email):
        mock_send_email.return_value = None
        self.client.login(email="creator@example.com", password="password")
        response = self.client.post(self.url, {
            "name": "Updated Event",
            "start_datetime": now(),
            "end_datetime": now() + timedelta(hours=3),
            "location": "Updated Location",
            "capacity": 25,
            "activity_type": self.activity.id,
            "description": "Updated description for the event.",
            "registration_status": "Open",
        })
        print(response.context['form'].errors if response.context else "No form in context")

        self.assertEqual(response.status_code, 302)
        self.event.refresh_from_db()
        self.assertEqual(self.event.name, "Updated Event")
        self.assertEqual(self.event.location, "Updated Location")
        self.assertEqual(self.event.capacity, 25)


class LeaveEventTestCase(TestCase):
    @patch("outdoor_buddy.accounts.signals.send_welcome_email_to_user")
    def setUp(self, mock_send_email):
        mock_send_email.return_value = None
        self.client = Client()

        self.user = UserModel.objects.create_user(email="participant@example.com", password="password")

        self.activity = Activity.objects.create(name="Hiking")
        self.event = Event.objects.create(
            name="Leaveable Event",
            start_datetime=now(),
            end_datetime=now() + timedelta(hours=3),
            location="Test Location",
            capacity=10,
            activity_type=self.activity,
            creator=self.user,
        )

        EventParticipant.objects.create(user=self.user, event=self.event)

        self.url = reverse("leave-event", kwargs={"event_id": self.event.id})

    @patch("outdoor_buddy.accounts.signals.send_welcome_email_to_user")
    def test_leave_event(self, mock_send_email):
        mock_send_email.return_value = None

        self.client.login(email="participant@example.com", password="password")
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertFalse(EventParticipant.objects.filter(user=self.user, event=self.event).exists())


class JoinFullyBookedEventTestCase(TestCase):
    @patch("outdoor_buddy.accounts.signals.send_welcome_email_to_user")
    def setUp(self, mock_send_email):
        mock_send_email.return_value = None

        self.client = Client()

        self.user = UserModel.objects.create_user(email="participant@example.com", password="password")
        self.another_user = get_user_model().objects.create_user(email="another@example.com", password="password")

        self.activity = Activity.objects.create(name="Hiking")
        self.event = Event.objects.create(
            name="Fully Booked Event",
            start_datetime=now(),
            end_datetime=now() + timedelta(hours=3),
            location="Test Location",
            capacity=1,
            activity_type=self.activity,
            creator=self.user,
        )

        EventParticipant.objects.create(user=self.user, event=self.event)

        self.url = reverse("join-event", kwargs={"event_id": self.event.id})

    @patch("outdoor_buddy.accounts.signals.send_welcome_email_to_user")
    def test_join_fully_booked_event(self, mock_send_email):
        mock_send_email.return_value = None

        self.client.login(email="another@example.com", password="password")
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertIn("This event is fully booked.", [m.message for m in messages])

        participants = EventParticipant.objects.filter(event=self.event).values_list("user__email", flat=True)
        self.assertNotIn("another@example.com", participants)

















