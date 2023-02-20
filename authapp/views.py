from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import request
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, UpdateView

from authapp import forms
from applicantapp.models import Applicants
from .models import CustomUser
from employerapp.models import Employer


class CustomLoginView(LoginView):
    def form_valid(self, form):
        ret = super().form_valid(form)
        message = _("Login success!<br>Hi, %(username)s") % {"username": self.request.user.get_username()}
        messages.add_message(self.request, messages.INFO, mark_safe(message))
        return ret

    def form_invalid(self, form):
        for _unused, msg in form.error_messages.items():
            messages.add_message(
                self.request,
                messages.WARNING,
                mark_safe(f"Something goes worng:<br>{msg}"),
            )
        return self.render_to_response(self.get_context_data(form=form))


class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.add_message(self.request, messages.INFO, _("See you later!"))
        return super().dispatch(request, *args, **kwargs)


class RegisterView(CreateView):
    model = get_user_model()
    form_class = forms.CustomUserCreationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("hhapp:main_page")


class ProfileEditView(UserPassesTestMixin, UpdateView):
    model = get_user_model()
    form_class = forms.CustomUserChangeForm
    template_name = "profile/profile_edit.html"

    def test_func(self):
        return True if self.request.user.pk == self.kwargs.get("pk") else False

    def get_success_url(self):
        return reverse_lazy("authapp:profile_edit", args=[self.request.user.pk])


def profile_info(request):
    form = CustomUser
    if request.user.is_company:
        if Employer.objects.filter(user=request.user):
            return render(request, "profile/profile_info.html", {"form": form})
        else:
            return redirect('employerapp:employer_create')
    else:
        if Applicants.objects.filter(user=request.user):
            return render(request, "profile/profile_info.html", {"form": form})
        else:
            return redirect('applicantapp:create')



