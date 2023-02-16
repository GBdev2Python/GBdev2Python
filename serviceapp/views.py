from django.shortcuts import render, get_object_or_404, redirect
from .models import Response
from employerapp.models import VacancyHeader
from .forms import ResponseForm
from django.contrib import messages

def response(request, vacancyheader):
    if request.user.is_authenticated:
        vacancy = VacancyHeader.objects.get(id=vacancyheader)
        print(request)
        if request.method == 'POST':
            form = ResponseForm(request.POST)
            if form.is_valid():
                resp = form.save(commit=False)
                resp.vacancyheader = vacancy
                resp.save()
                return redirect('/news/')
            else:
                messages.error(request, 'Ошибка отправки отклика')
        else:
            form = ResponseForm()
    else:
        messages.error(request, 'Пользователь не авторизовон')
        form = {}
    return render(request, 'serviceapp/response.html', {"form": form})
