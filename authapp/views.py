from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, \
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.views.generic import UpdateView, ListView
from django.db.models import Count, When, Case

from authapp import forms
from applicantapp.models import Applicants
from .forms import CustomUserCreationForm, CustomModeratorUserEditForm
from .models import CustomUser
from employerapp.models import Employer


class CustomLoginView(LoginView):

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(reverse_lazy('hhapp:main_page'))

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        super().form_valid(form)
        message = _("Login success!<br>Hi, %(username)s") % {"username": self.request.user.get_username()}
        messages.add_message(self.request, messages.INFO, mark_safe(message))
        messages.add_message(
            self.request,
            messages.WARNING,
            mark_safe(f'is_comp:{self.request.user.is_company}'
                      f'<br>name:{self.request.user.username}')
        )
        if self.request.GET.get("next") is not None:
            return redirect(self.request.GET.get("next"))
        return redirect('authapp:profile_info')

    def form_invalid(self, form):
        for _, message in form.error_messages.items():
            messages.add_message(
                self.request,
                messages.WARNING,
                mark_safe(f"An error occurred:<br>{message}"),
            )
        return self.render_to_response(self.get_context_data(form=form))


class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.add_message(self.request, messages.INFO, _("See you later!"))
        return super().dispatch(request, *args, **kwargs)


class ProfileEditView(UserPassesTestMixin, UpdateView):
    login_url = reverse_lazy('authapp:login')
    model = get_user_model()
    form_class = forms.CustomUserChangeForm
    template_name = "registration/profile_edit.html"

    def test_func(self):
        return True if self.request.user.pk == self.kwargs.get("pk") else False

    def get_success_url(self):
        return reverse_lazy("authapp:profile_edit", args=[self.request.user.pk])


def profile_info(request):
    if request.user.is_company:
        if Employer.objects.filter(user=request.user):
            user = Employer.objects.get(user_id=request.user.id).id
            return HttpResponseRedirect(reverse_lazy('employerapp:employer_cabinet', args=(user,)))
        else:
            return redirect('employerapp:employer_create')
    else:
        if Applicants.objects.filter(user=request.user):
            user = Applicants.objects.get(user_id=request.user.id).id
            return HttpResponseRedirect(reverse_lazy('applicant:applicant_cabinet', args=(user,)))
        else:
            return redirect('applicantapp:create')


def register(request):
    if not request.user.is_anonymous:
        return redirect(reverse_lazy('hhapp:main_page'))

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='authapp.backends.EmailandUserBackend')
            return redirect('authapp:profile_info')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {"form": form})


class CustomPasswordChangeView(UserPassesTestMixin, PasswordChangeView):
    template_name = "registration/custom_password_change.html"
    success_url = reverse_lazy("authapp:password_change_done")

    def dispatch(self, request, *args, **kwargs):
        user_test_resul = self.get_test_func()()
        if not user_test_resul:
            return redirect(reverse_lazy('authapp:password_change', args=(self.request.user.id, )))
        return super().dispatch(request, *args, **kwargs)

    def test_func(self):
        return self.request.user.pk == self.kwargs.get('pk')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.add_message(self.request, messages.INFO, message=f'Password has been successfully changed')
        return response


class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'registration/custom_password_change_done.html'


class CustomPasswordResetView(PasswordResetView):
    template_name = 'registration/custom_password_reset_form.html'
    success_url = reverse_lazy("authapp:password_reset_done")
    form_class = forms.CustomPasswordResetForm
    email_template_name = 'registration/custom_password_reset_email.html'

    def form_valid(self, form):
        opts = {
            "use_https": self.request.is_secure(),
            "token_generator": self.token_generator,
            "from_email": self.from_email,
            "email_template_name": self.email_template_name,
            "subject_template_name": self.subject_template_name,
            "request": self.request,
            "html_email_template_name": self.html_email_template_name,
            "extra_email_context": self.extra_email_context,
        }
        form.save(**opts)
        return super().form_valid(form)


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'registration/custom_password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy('authapp:password_reset_complete')
    template_name = 'registration/custom_password_reset_confirm.html'


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'registration/custom_password_reset_complete_view.html'


class UserModerationView(UserPassesTestMixin, ListView):
    queryset = CustomUser.objects.select_related('applicants', 'employer') \
        .annotate(
        cab_a=Count('applicants__id'),
        cab_e=Count('employer__id'),
        role=Case(When(is_company=1, then='employer__id'), When(is_company=0, then='applicants__id')),
    ).only('is_active', 'username', 'is_company')
    model = CustomUser
    template_name = 'authapp/moderation.html'
    context_object_name = 'users'
    ordering = ['is_active', '-is_company', 'email']

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['username_parameter'] = self.request.GET.get("username", "")
        context['status_selected'] = int(self.request.GET.get("user_status", -1))
        return context

    def test_func(self):
        return True if self.request.user.is_staff or self.request.user.is_superuser else False

    def get_queryset(self, *args, **kwargs):
        if self.request.GET:
            queryset = self.queryset
            user_status = int(self.request.GET.get("user_status"))

            if user_status >= 0:
                queryset = queryset.filter(is_company=user_status)
            if self.request.GET.get("username") is not None:
                queryset = queryset.filter(username__icontains=self.request.GET.get("username"))

            return queryset.order_by(*self.ordering)

        return self.queryset.order_by(*self.ordering)


class UserModeratorEditView(UserPassesTestMixin, UpdateView):
    model = get_user_model()
    form_class = CustomModeratorUserEditForm
    template_name = "registration/profile_edit.html"
    success_url = reverse_lazy("authapp:moderation")

    def test_func(self):
        user_is_owner = self.request.user.pk == self.kwargs.get("pk")
        user_is_staff_or_admin = self.request.user.is_superuser or self.request.user.is_staff
        return True if user_is_owner or user_is_staff_or_admin else False
