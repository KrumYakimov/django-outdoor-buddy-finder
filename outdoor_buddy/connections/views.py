from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.views.generic import ListView

from outdoor_buddy.accounts.models import Profile, Contact
from outdoor_buddy.connections.choices import StatusChoices
from outdoor_buddy.connections.models import BuddyRequest, Connection

UserModel = get_user_model()


# class SendBuddyRequestView(LoginRequiredMixin, View):
#     def post(self, request, *args, **kwargs):
#         to_user_id = kwargs.get("user_id")
#         to_user = get_object_or_404(UserModel, id=to_user_id)
#
#         if request.user == to_user:
#             messages.error(request, "You cannot send a buddy request to yourself.")
#             return redirect("profile", pk=to_user.pk)
#
#         if BuddyRequest.objects.filter(
#             from_user=request.user, to_user=to_user
#         ).exists():
#             messages.warning(
#                 request, "You have already sent a buddy request to this user."
#             )
#             return redirect("profile", pk=to_user.pk)
#
#         BuddyRequest.objects.create(from_user=request.user, to_user=to_user)
#         messages.success(request, "Buddy request sent successfully!")
#         return redirect("profile", pk=to_user.pk)
#
#
# class RespondBuddyRequestView(LoginRequiredMixin, View):
#     def post(self, request, *args, **kwargs):
#         request_id = kwargs.get("request_id")
#         action = request.POST.get("action")  # Expected values: 'accept' or 'decline'
#
#         buddy_request = get_object_or_404(
#             BuddyRequest, id=request_id, to_user=request.user
#         )
#
#         if action == "accept":
#             # Ensure no duplicate connections are created
#             connection_exists = Connection.objects.filter(
#                 Q(user1=buddy_request.from_user, user2=buddy_request.to_user) |
#                 Q(user1=buddy_request.to_user, user2=buddy_request.from_user)
#             ).exists()
#
#             if not connection_exists:
#                 # Create the connection
#                 Connection.objects.create(
#                     user1=buddy_request.from_user, user2=buddy_request.to_user
#                 )
#             buddy_request.status = StatusChoices.ACCEPTED
#             buddy_request.save()
#             messages.success(request, "You have accepted the buddy request.")
#         elif action == "decline":
#             buddy_request.status = StatusChoices.DECLINED
#             buddy_request.save()
#             messages.success(request, "You have declined the buddy request.")
#         else:
#             messages.error(request, "Invalid action.")
#
#         return redirect("profile", pk=buddy_request.from_user.pk)
#
#
# class DisconnectBuddyView(LoginRequiredMixin, View):
#     def post(self, request, *args, **kwargs):
#         # Get the user to disconnect
#         user_id = kwargs.get("user_id")
#         other_user = get_object_or_404(UserModel, id=user_id)
#
#         # Delete the connection if it exists
#         connection = Connection.objects.filter(
#             Q(user1=request.user, user2=other_user) |
#             Q(user1=other_user, user2=request.user)
#         ).first()
#
#         if connection:
#             connection.delete()
#             messages.success(request, "You have successfully disconnected.")
#         else:
#             messages.error(request, "You are not connected to this user.")
#
#         return redirect("profile", pk=user_id)

class SendBuddyRequestView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        to_user_id = kwargs.get("user_id")
        to_user = get_object_or_404(UserModel, id=to_user_id)

        BuddyRequest.objects.create(from_user=request.user, to_user=to_user)
        return redirect("request-sent")


class RespondBuddyRequestView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        request_id = kwargs.get("request_id")
        action = request.POST.get("action")

        buddy_request = get_object_or_404(
            BuddyRequest, id=request_id, to_user=request.user
        )

        if action == "accept":
            connection_exists = Connection.objects.filter(
                Q(user1=buddy_request.from_user, user2=buddy_request.to_user) |
                Q(user1=buddy_request.to_user, user2=buddy_request.from_user)
            ).exists()

            if not connection_exists:
                Connection.objects.create(
                    user1=buddy_request.from_user, user2=buddy_request.to_user
                )
            buddy_request.status = StatusChoices.ACCEPTED
            buddy_request.save()
            return redirect("request-accepted")
        elif action == "decline":
            buddy_request.status = StatusChoices.DECLINED
            buddy_request.save()
            return redirect("request-declined")


# class DisconnectBuddyView(LoginRequiredMixin, View):
#     def post(self, request, *args, **kwargs):
#         user_id = kwargs.get("user_id")
#         other_user = get_object_or_404(UserModel, id=user_id)
#
#         connection = Connection.objects.filter(
#             Q(user1=request.user, user2=other_user) |
#             Q(user1=other_user, user2=request.user)
#         ).first()
#
#         if connection:
#             connection.delete()
#             return redirect("disconnect-success")

class DisconnectBuddyView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user_id = kwargs.get("user_id")
        other_user = get_object_or_404(UserModel, id=user_id)

        # Delete the connection from the Connection table
        connection = Connection.objects.filter(
            Q(user1=request.user, user2=other_user) |
            Q(user1=other_user, user2=request.user)
        ).first()

        if connection:
            connection.delete()

        # Delete any related BuddyRequest entries from the BuddyRequest table
        BuddyRequest.objects.filter(
            Q(from_user=request.user, to_user=other_user) |
            Q(from_user=other_user, to_user=request.user)
        ).delete()

        return redirect("disconnect-success")


def request_sent_view(request):
    return render(request, "connections/request-sent.html")


def request_accepted_view(request):
    return render(request, "connections/request-accepted.html")


def request_declined_view(request):
    return render(request, "connections/request-declined.html")


def disconnect_success_view(request):
    return render(request, "connections/disconnect-success.html")


class ConnectedProfilesView(LoginRequiredMixin, ListView):
    model = Profile
    template_name = "connections/connected-profiles.html"
    context_object_name = "profiles"
    paginate_by = 6

    def get_queryset(self):
        # Fetch connected users
        user = self.request.user
        connected_user_ids = Connection.objects.filter(
            Q(user1=user) | Q(user2=user)
        ).values_list("user1", "user2")

        # Collect unique connected user IDs (excluding the logged-in user)
        connected_ids = set()
        for user1, user2 in connected_user_ids:
            connected_ids.add(user1 if user1 != user.id else user2)

        return Profile.objects.filter(user_id__in=connected_ids).select_related("user")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add current user's profile and contact explicitly
        context["my_profile"] = Profile.objects.get(user=self.request.user)
        context["my_contact"] = Contact.objects.get(user=self.request.user)

        return context


