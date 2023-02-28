from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.template import context
from django.views.generic import CreateView

from applicantapp.models import Resumes, Applicants
from .models import Response
from employerapp.models import VacancyHeader, Employer
from .forms import ResponseForm, ResponseChangeStatusForm
from django.contrib import messages


# class ResponseCreate(LoginRequiredMixin, CreateView):
#     form_class = ResponseForm
#     template_name = "serviceapp/response.html"
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["resume"] = Resumes.objects.filter(id=Employer.objects.get(id = self.request.user.applicants.id).id)
#         #print(context["resume"])
#         return context


def response(request, vacancyheader):
    if request.user.is_authenticated:
        vacancy = VacancyHeader.objects.get(id=vacancyheader)
        if request.method == 'POST':
            form = ResponseForm(request.POST)
            resume = Resumes.objects.get(id=request.POST['resume_id'])
            if form.is_valid():
                resp = form.save(commit=False)
                resp.vacancyheader = vacancy
                resp.resume = resume
                resp.save()
                return redirect('/news/')
            else:
                messages.error(request, 'Ошибка отправки отклика')
        else:
            form = ResponseForm()
    else:
        messages.error(request, 'Пользователь не авторизовон')
        form = {}
    applicant = Applicants.objects.get(id = request.user.applicants.id).id
    resume = Resumes.objects.all().filter(applicants_id=applicant)
    print(resume.count)
    if resume.count() == 0:
        return redirect('applicantapp:new_resume', applicant_id = applicant)
    return render(request, 'serviceapp/response.html', {"form": form, "resume": resume})


def response_view(request, response_id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            print(request.POST)
            response_change = Response.objects.get(id=response_id)
            response_change.status = request.POST['status']
            response_change.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            form = ResponseChangeStatusForm()
    else:
        messages.error(request, 'Пользователь не авторизовон')
        form = {}
    return render(request, 'serviceapp/response_view.html', {"form": form, "response": Response.objects.get(id=response_id)})


