from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import View
from outdoor_buddy.events.models import Event
from outdoor_buddy.reviews.models import Review
from outdoor_buddy.reviews.forms import ReviewForm


class SubmitReviewView(View):
    def post(self, request, pk, *args, **kwargs):
        """
        Handle the submission of a review for a hiking event.
        """
        event = get_object_or_404(Event, pk=pk)
        rating = request.POST.get("rating")
        comment = request.POST.get("comment")

        if not rating or not (1 <= int(rating) <= 5):
            messages.error(request, "Invalid rating. Please provide a rating between 1 and 5.")
            return redirect("event-detail", pk=pk)

        review, created = Review.objects.update_or_create(
            reviewer=request.user,
            event=event,
            defaults={"rating": rating, "comment": comment},
        )

        # if created:
        #     messages.success(request, "Thank you for leaving a review!")
        # else:
        #     messages.success(request, "Your review has been updated.")

        return redirect("event-detail", pk=pk)
