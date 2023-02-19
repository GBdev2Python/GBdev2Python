from django.shortcuts import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import TemplateView, ListView, CreateView

from applicantapp.forms import ResumeForm, AddApplicateForm
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
        profiles = Resumes.objects.all()
        context = super().get_context_data(**kwargs)
        context["resume_list"] = profiles
        # context["skills"] = profiles.skills.all()[:2]
        # print(context["resume_list"])
        return context


# Отдельное резюме для работодателя
class Resume(ListView):
    model = Resumes
    template_name = "applicantapp/resume.html"

    def get_context_data(self, **kwargs):
        profile = Resumes.objects.get(id=self.kwargs["resume_id"])
        context = super().get_context_data(**kwargs)
        context["resume"] = profile
        context["skills"] = profile.skills.all()
        return context


# Отдельное резюме для соискателя
class ApplicantResume(ListView):
    model = Resumes
    template_name = "applicantapp/applicant_resume.html"

    def get_context_data(self, **kwargs):
        profile = Resumes.objects.get(id=self.kwargs["resume_id"])
        context = super().get_context_data(**kwargs)
        context["resume"] = profile
        context["skills"] = profile.skills.all()
        return context

# Заполнение профиля соискателя
class ApplicantCreate(CreateView):
    form_class = AddApplicateForm
    template_name = "applicantapp/applicant_create.html"


class ApplicantCabinet(TemplateView):
    template_name = "applicantapp/applicant_cabinet.html"
    pk_url_kwarg = "applicant_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["applicant_list"] = Applicants.objects.all()
        context["applicant"] = Applicants.objects.get(id=self.kwargs["applicant_id"])
        context["resumes"] = Resumes.objects.filter(applicants=self.kwargs["applicant_id"])

        return context



# Отдельный соискатель
class Applicant(ListView):
    model = Applicants
    template_name = "applicantapp/applicant.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context["applicant"] = Applicants.objects.get(id=self.kwargs["applicant_id"])
        context["resumes"] = Resumes.objects.filter(applicants=self.kwargs["applicant_id"])
        return context


# Создание резюм
def new_resume(request, applicant_id, *args, **kwargs):
    user = Applicants.objects.get(id=applicant_id)
    form = ResumeForm(initial={'applicants': user})
    if request.method == "POST":
        form = ResumeForm(request.POST, request.FILES)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.applicants = user
            resume.save()
            form.save_m2m()
        return redirect("applicant:applicant_cabinet", applicant_id=resume.applicants.id)

    context = {"form": form, "applicant": user}
    return render(request, "applicantapp/new_resume.html", context)


# Внесение изменений в резюме
def update_resume(request, pk):
    form = ResumeForm()
    resume = Resumes.objects.get(id=pk)
    user = Applicants.objects.get(id=resume.applicants.id)
    form = ResumeForm(instance=resume)

    if request.method == "POST":
        form = ResumeForm(request.POST, request.FILES, instance=resume)

        if form.is_valid():
            resume = form.save()
            return redirect("applicant:applicant_cabinet", applicant_id=user.id)

    context = {"form": form, "applicant": user}
    return render(request, "applicantapp/new_resume.html", context)


# Удаление резюме соискателя
def delete_resume(request, pk):

    resume = Resumes.objects.get(id=pk)
    if request.method == "POST":
        resume.delete()
        return redirect("applicant:applicant_cabinet", applicant_id=resume.applicants.id)
    context = {"object": resume}
    return render(request, "applicantapp/delete_resume.html", context)
