from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView


class MainPageView(TemplateView):
    template_name = "hhapp/home.html"
