from django.urls import path
from django.views.generic import TemplateView

from outdoor_buddy.core import views

urlpatterns = [
    path("", views.HomePageView.as_view(), name="home"),
    path("about/", TemplateView.as_view(template_name="core/about.html"), name="about"),
]
