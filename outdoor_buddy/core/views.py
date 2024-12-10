from django.http import JsonResponse
from django.views import generic as views


class HomePageView(views.TemplateView):
    template_name = "core/home-page.html"


def health_check(request):
    return JsonResponse({"status": "ok"})
