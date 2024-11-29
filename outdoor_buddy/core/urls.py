from django.urls import path
from outdoor_buddy.core import views

urlpatterns = [
    path("", views.HomePageView.as_view(), name="home"),
]