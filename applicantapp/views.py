from django.db.models import Q, Prefetch
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from applicantapp.forms import ResumeForm, EditApplicantForm, InvitationCreationForm, ExperienceFormSet, \
    ExperienceEditFormset
from applicantapp.models import *
from .utils import save_experience_data, validate_experience_subform, update_experience_data
from serviceapp.models import Response
from django.contrib.auth.decorators import login_required


class ApplicantList(ListView):
    model = Applicants
    template_name = "applicantapp/applicant_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["applicant_list"] = Applicants.objects.all()
        return context


class ResumeList(ListView):
    model = Resumes
    template_name = "applicantapp/resume_list.html"

    def get_context_data(self, **kwargs):
        profiles = Resumes.objects.all()
        context = super().get_context_data(**kwargs)
        context["resume_list"] = profiles
        return context


# Отдельное резюме для работодателя
class Resume(DetailView):
    model = Resumes
    pk_url_kwarg = 'resume_id'
    template_name = "applicantapp/resume.html"
    context_object_name = 'resume'

    def get_object(self, queryset=None):
        resume = Resumes.objects \
            .select_related('applicants', 'applicants__user', 'applicants__town') \
            .prefetch_related('skills',
                              Prefetch(
                                  'experience', queryset=Experience.objects.all()
                                  .only('company', 'description', 'resume_id'))
                              ) \
            .only('applicants__first_name', 'applicants__last_name', 'applicants__birthday',
                  'applicants__town__town', 'applicants__phone', 'applicants__user__email',
                  'salary', 'required_job', 'education', 'education', 'image',
                  'skills__name',
                  ) \
            .get(id=self.kwargs["resume_id"])
        return resume

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_company:
            response = ResumeInvitation.objects \
                .select_related("vacancy", "vacancy__employer__user") \
                .filter(Q(vacancy__employer__user__id=self.request.user.id) & Q(resume_id=self.kwargs["resume_id"])) \
                .only("id", "vacancy__employer__user_id", "vacancy_id", 'cover_letter', 'status')
            context["response"] = response.first() if response.exists() else False

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
        if self.request.user.id == profile.applicants.user.id:
            context["response"] = Response.objects.all().filter(resume=profile)
        return context


# Заполнение профиля соискателя
class ApplicantCreate(CreateView):
    model = Applicants
    fields = ["image", "first_name", "last_name", "birthday", "town", "phone"]
    labels = {
        "image": "Аватар",
        "first_name": "Имя",
        "last_name": "Фамилия",
        "birthday": "Дата рождения",
        "town": "Город (населенный пункт)",
    }
    template_name = "applicantapp/applicant_create.html"

    def form_valid(self, form):
        new_applicant = form.save()
        new_applicant.user = self.request.user
        new_applicant.save()
        return redirect("applicant:applicant_cabinet", applicant_id=new_applicant.id)


# Редактирование профиля соискателя
@login_required()
def update_applicant(request, pk):
    applicant = Applicants.objects.get(id=pk)
    form = EditApplicantForm(instance=applicant)

    if request.user.is_authenticated and Applicants.objects.get(user=request.user).id == applicant.id:
        if request.method == "POST":
            form = EditApplicantForm(request.POST, request.FILES, instance=applicant)

            if form.is_valid():
                form.save()
                return redirect("applicant:applicant_cabinet", applicant_id=applicant.id)

        context = {"form": form}
        return render(request, "applicantapp/applicant_edit.html", context)
    else:
        return redirect("applicant:applicant_cabinet", applicant_id=Applicants.objects.get(user=request.user).id)


class ApplicantCabinet(LoginRequiredMixin, ListView):
    model = Resumes
    template_name = "applicantapp/applicant_cabinet.html"
    pk_url_kwarg = "applicant_id"
    paginate_by = 3

    def get_queryset(self, **kwargs):
        return Resumes.objects.filter(applicants=self.kwargs["applicant_id"])

    def get_context_data(self, **kwargs):
        profile = self.request.user.applicants
        messageRequests = Response.objects.filter(resume__applicants=profile.id)
        resumeID = set()
        for i in messageRequests:
            resumeID.add(i.resume.id)
        queryset = Resumes.objects.filter(applicants=self.kwargs["applicant_id"])
        resumes = Resumes.objects.filter(applicants=self.kwargs["applicant_id"])
        context = super().get_context_data(**kwargs)
        context["applicant_list"] = Applicants.objects.all()
        context["applicant"] = Applicants.objects.get(id=self.kwargs["applicant_id"])
        context["resumes"] = resumes
        context["queryset"] = queryset
        context["resumeID"] = resumeID
        return context

    def dispatch(self, request, *args, **kwargs):
        user_URL = Applicants.objects.get(id=self.kwargs["applicant_id"])
        user_authenticated = Applicants.objects.get(user=request.user)

        if request.user.is_authenticated and user_URL == user_authenticated:
            return super().dispatch(request, *args, **kwargs)
        return self.handle_no_permission()


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
@login_required()
def new_resume(request, applicant_id, *args, **kwargs):
    user = Applicants.objects.get(id=applicant_id)
    form = ResumeForm(initial={'applicants': user})

    if request.user.is_authenticated and user.id == Applicants.objects.get(user=request.user).id:
        if request.method == "POST":
            form = ResumeForm(request.POST, request.FILES)
            if form.is_valid():
                resume = form.save(commit=False)
                resume.applicants = user
                resume.save()
                form.save_m2m()

                valid_experience_fields = validate_experience_subform(request.POST)
                if valid_experience_fields:
                    save_experience_data(valid_experience_fields, resume)

            return redirect("applicant:applicant_cabinet", applicant_id=resume.applicants.id)

        context = {"form": form, "applicant": user, "experience_formset": ExperienceFormSet()}

        return render(request, "applicantapp/new_resume.html", context)
    else:
        return redirect("applicant:applicant_cabinet", applicant_id=Applicants.objects.get(user=request.user).id)


# Внесение изменений в резюме
@login_required()
def update_resume(request, pk):
    resume = Resumes.objects.get(pk=pk)
    user = Applicants.objects.get(id=resume.applicants.id)
    form = ResumeForm(instance=resume)

    formset = ExperienceEditFormset(queryset=Experience.objects.filter(resume=resume).order_by('created'))

    if request.user.is_authenticated and Applicants.objects.get(user=request.user).id == resume.applicants.id:
        if request.method == "POST":
            form = ResumeForm(request.POST, request.FILES, instance=resume)
            if form.is_valid():
                valid_experience_fields = update_experience_data(request.POST, resume=resume)
                print(valid_experience_fields)
                resume = form.save()
                return redirect("applicant:applicant_cabinet", applicant_id=user.id)

        context = {"form": form, "applicant": user, 'experience_formset': formset}
        return render(request, "applicantapp/new_resume.html", context)
    else:
        return redirect("applicant:applicant_cabinet", applicant_id=Applicants.objects.get(user=request.user).id)


# Удаление резюме соискателя
@login_required()
def delete_resume(request, pk):
    resume = Resumes.objects.get(id=pk)
    if request.user.is_authenticated and Applicants.objects.get(user=request.user).id == resume.applicants.id:
        if request.method == "POST":
            applicantID = resume.applicants.pk
            resume.delete()
            return redirect("applicant:applicant_cabinet", applicant_id=applicantID)
        context = {"object": resume}
        return render(request, "applicantapp/delete_resume.html", context)
    else:
        return redirect("applicant:applicant_cabinet", applicant_id=Applicants.objects.get(user=request.user).id)


class ResumeInvitationCreation(UserPassesTestMixin, CreateView):
    model = ResumeInvitation
    form_class = InvitationCreationForm
    template_name = 'applicantapp/invitation_create.html'

    def get_context_data(self, **kwargs):
        print(self.kwargs.get('resume_pk'))
        context = super().get_context_data(**kwargs)
        resume_data = Resumes.objects \
            .select_related('applicants__user') \
            .only('id', 'applicants__user__email', 'applicants__phone', 'applicants__first_name',
                  'applicants__last_name', 'required_job', 'salary', 'education') \
            .get(pk=self.kwargs.get('resume_pk'))

        context['resume_data'] = resume_data
        return context

    def test_func(self):
        user_is_company = self.request.user.is_company
        company_didnt_invite_this_resume = ResumeInvitation.objects \
            .select_related("vacancy", "vacancy__employer__user") \
            .filter(Q(vacancy__employer__user__id=self.request.user.id) & Q(resume_id=self.kwargs["resume_pk"])) \
            .only("id", "vacancy__employer__user_id", "vacancy_id", 'cover_letter', 'status')

        return user_is_company and not company_didnt_invite_this_resume

    def dispatch(self, request, *args, **kwargs):
        if self.get_test_func()():
            return super().dispatch(request, *args, **kwargs)

        return redirect(reverse('applicant:resume_by_id', kwargs={'resume_id': self.kwargs['resume_pk']}))

    def get_success_url(self, **kwargs):
        return reverse_lazy('applicant:resume_by_id', kwargs={"resume_id": self.kwargs.get('resume_pk')})

    def get_form(self, form_class=None):
        ret_form = super().get_form(form_class=form_class)
        ret_form.fields['resume'].initial = self.kwargs.get('resume_pk')
        ret_form.fields['vacancy'].queryset = self.request.user.employer.vacancies.all()
        return ret_form
