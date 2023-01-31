from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, TemplateView
from applicantapp.models import *

# Create your views here.

# Список соискателей
class ApplicantList(ListView):
    model = Applicants
    template_name = "applicantapp/applicant_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["applicant_list"] = Applicants.objects.all()
        return context

# Список резюме
class ResumeList(ListView):
    model = Resumes
    template_name = "applicantapp/resume_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["resume_list"] = Resumes.objects.all()
        print(context["resume_list"])
        return context

# Отдельное резюме
class Resume(ListView):
    model = Resumes
    template_name = "applicantapp/resume.html"

    def get_context_data(self, **kwargs):
        profile = Resumes.objects.get(id = self.kwargs['resume_id'])
        context = super().get_context_data(**kwargs)
        context["resume"] = profile
        context["skills"] = profile.skills.all()[:2]
        return context

# Отдельный соискатель
class Applicant(ListView):
    model = Applicants
    template_name = "applicantapp/applicant.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context["applicant"] = Applicants.objects.get(id = self.kwargs['applicant_id'])
        return context
