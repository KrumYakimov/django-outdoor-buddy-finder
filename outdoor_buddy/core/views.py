from django.shortcuts import render
from django.views import generic as views


class HomePageView(views.TemplateView):
    template_name = "core/home-page.html"
