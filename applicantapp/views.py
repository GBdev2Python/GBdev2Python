from django.shortcuts import render, get_object_or_404,redirect
from django.views.generic import ListView, TemplateView
from applicantapp.models import *
from applicantapp.forms import ResumeForm

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
        #context["skills"] = profiles.skills.all()[:2]
        #print(context["resume_list"])
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
        context["resumes"] = Resumes.objects.filter(applicants = self.kwargs['applicant_id'])
        return context


# Создание резюме
def new_resume(request):
    form = ResumeForm()

    if request.method == 'POST':
        form = ResumeForm(request.POST)
        if form.is_valid():
            resume =form.save()
            return redirect(resume)
    else:
        form = ResumeForm()
    context = {'form': form}
    return render(request,'applicantapp/new_resume.html', context)

# Внесение изменений в резюме

def update_resume(request, applicant_id):
    form = ResumeForm()
    resume = request.user.profile
  #  project = profile.project_set.get(id=pk)
   # form = ProjectForm(instance=project)

   # if request.method == 'POST':
    #    newtags = request.POST.get('newtags').replace(',',  " ").split()

     #   form = ProjectForm(request.POST, request.FILES, instance=project)
      #  if form.is_valid():
       #     project = form.save()
        #    for tag in newtags:
         #       tag, created = Tag.objects.get_or_create(name=tag)
          #      project.tags.add(tag)

     #       return redirect('account')

   # context = {'form': form, 'project': project}
    context = {'form': form}
    return render(request,'applicantapp/new_resume.html', context)


