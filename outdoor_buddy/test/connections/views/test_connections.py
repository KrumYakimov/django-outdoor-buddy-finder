from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from outdoor_buddy.connections.choices import StatusChoices
from outdoor_buddy.connections.models import BuddyRequest, Connection

UserModel = get_user_model()


class SendBuddyRequestViewTestCase(TestCase):
    @patch("outdoor_buddy.accounts.signals.send_welcome_email_to_user")
    def setUp(self, mock_send_email):
        mock_send_email.return_value = None

        self.client = Client()
        self.user1 = UserModel.objects.create_user(
            email="user1@example.com", password="password"
        )
        self.user2 = UserModel.objects.create_user(
            email="user2@example.com", password="password"
        )
        self.url = reverse("send-buddy-request", kwargs={"user_id": self.user2.id})

    @patch("outdoor_buddy.accounts.signals.send_welcome_email_to_user")
    def test_send_new_buddy_request(self, mock_send_email):
        mock_send_email.return_value = None

        self.client.login(email="user1@example.com", password="password")
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 302)
        buddy_request = BuddyRequest.objects.get(
            from_user=self.user1, to_user=self.user2
        )
        self.assertEqual(buddy_request.status, "Pending")

    @patch("outdoor_buddy.accounts.signals.send_welcome_email_to_user")
    def test_reactivate_declined_request(self, mock_send_email):
        mock_send_email.return_value = None

        BuddyRequest.objects.create(
            from_user=self.user1, to_user=self.user2, status="Declined"
        )

        self.client.login(email="user1@example.com", password="password")
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 302)
        buddy_request = BuddyRequest.objects.get(
            from_user=self.user1, to_user=self.user2
        )
        self.assertEqual(buddy_request.status, "Pending")

    @patch("outdoor_buddy.accounts.signals.send_welcome_email_to_user")
    def test_send_request_to_self_returns_403(self, mock_send_email):
        mock_send_email.return_value = None

        self.client.login(email="user1@example.com", password="password")
        url = reverse("send-buddy-request", kwargs={"user_id": self.user1.id})
        response = self.client.post(url)

        self.assertEqual(
            response.status_code, 403
        )  # Expect 403 response for self-request
        self.assertFalse(
            BuddyRequest.objects.filter(
                from_user=self.user1, to_user=self.user1
            ).exists()
        )


class RespondBuddyRequestViewTestCase(TestCase):
    @patch("outdoor_buddy.accounts.signals.send_welcome_email_to_user")
    def setUp(self, mock_send_email):
        mock_send_email.return_value = None

        self.client = Client()
        self.user1 = UserModel.objects.create_user(
            email="user1@example.com", password="password"
        )
        self.user2 = UserModel.objects.create_user(
            email="user2@example.com", password="password"
        )
        self.buddy_request = BuddyRequest.objects.create(
            from_user=self.user1, to_user=self.user2
        )

    @patch("outdoor_buddy.accounts.signals.send_welcome_email_to_user")
    def test_accept_buddy_request_creates_connection(self, mock_send_email):
        mock_send_email.return_value = None

        self.client.login(email="user2@example.com", password="password")
        url = reverse(
            "respond-buddy-request", kwargs={"request_id": self.buddy_request.id}
        )
        response = self.client.post(url, {"action": "accept"})

        self.assertEqual(response.status_code, 302)
        self.buddy_request.refresh_from_db()
        self.assertEqual(self.buddy_request.status, StatusChoices.ACCEPTED)
        self.assertTrue(
            Connection.objects.filter(user1=self.user1, user2=self.user2).exists()
        )

    @patch("outdoor_buddy.accounts.signals.send_welcome_email_to_user")
    def test_decline_buddy_request(self, mock_send_email):
        mock_send_email.return_value = None

        self.client.login(email="user2@example.com", password="password")
        url = reverse(
            "respond-buddy-request", kwargs={"request_id": self.buddy_request.id}
        )
        response = self.client.post(url, {"action": "decline"})

        self.assertEqual(response.status_code, 302)
        self.buddy_request.refresh_from_db()
        self.assertEqual(self.buddy_request.status, StatusChoices.DECLINED)
        self.assertFalse(
            Connection.objects.filter(user1=self.user1, user2=self.user2).exists()
        )

    @patch("outdoor_buddy.accounts.signals.send_welcome_email_to_user")
    def test_invalid_request_raises_404(self, mock_send_email):
        mock_send_email.return_value = None

        self.client.login(email="user2@example.com", password="password")
        url = reverse(
            "respond-buddy-request", kwargs={"request_id": 999}
        )  # Non-existent ID
        response = self.client.post(url, {"action": "accept"})

        self.assertEqual(response.status_code, 404)


class DisconnectBuddyViewTestCase(TestCase):
    @patch("outdoor_buddy.accounts.signals.send_welcome_email_to_user")
    def setUp(self, mock_send_email):
        mock_send_email.return_value = None

        self.user1 = UserModel.objects.create_user(
            email="user1@example.com", password="password"
        )
        self.user2 = UserModel.objects.create_user(
            email="user2@example.com", password="password"
        )

        self.connection = Connection.objects.create(user1=self.user1, user2=self.user2)
        BuddyRequest.objects.create(
            from_user=self.user1, to_user=self.user2, status="Accepted"
        )

        self.client.login(email="user1@example.com", password="password")
        self.url = reverse("disconnect-buddy", kwargs={"user_id": self.user2.id})

    def test_disconnect_valid_connection(self):
        """Test that a valid connection is deleted."""
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)

        self.assertFalse(
            Connection.objects.filter(user1=self.user1, user2=self.user2).exists()
        )
        self.assertFalse(
            BuddyRequest.objects.filter(
                from_user=self.user1, to_user=self.user2
            ).exists()
        )

    def test_disconnect_no_connection(self):
        """Test that no errors occur when disconnecting without an existing connection."""
        self.connection.delete()

        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            BuddyRequest.objects.filter(
                from_user=self.user1, to_user=self.user2
            ).exists()
        )
