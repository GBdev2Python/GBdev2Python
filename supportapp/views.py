from django.core.mail import send_mail
from django.db.models import Prefetch
from django.http import JsonResponse
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from django.views.generic import ListView, FormView, TemplateView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.conf import settings

from .models import Ticket, TicketMessage
from .forms import CreateTicketForm, CreateTicketMessageForm, TicketChangeStatusForm


class TicketsListView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy("authapp:login")
    template_name = "supportapp/tickets.html"
    context_object_name = 'tickets'
    ordering = ['status', 'created']

    def get_queryset(self):
        queryset = Ticket.objects.all()

        is_not_staff_or_not_superuser = not self.request.user.is_staff and not self.request.user.is_superuser
        if is_not_staff_or_not_superuser:
            queryset = queryset.filter(user_id=self.request.user.id)

        queryset = queryset.select_related('user') \
            .only("id", "init_message", "created", "topic", "status", "user__username", "user__email", 'theme')

        if self.request.GET:
            if self.request.GET.get('theme') is not None:
                queryset = queryset.filter(theme__icontains=self.request.GET.get('theme'))

            topic = self.request.GET.get('topic')
            if topic:
                queryset = queryset.filter(topic=topic)

            status = self.request.GET.get('status')
            if status:
                queryset = queryset.filter(status=status)

            created = self.request.GET.get('created')
            if created:
                queryset = queryset.order_by(f"{'' if created == '+' else '-'}created")
                return queryset

        return queryset.order_by(*self.ordering)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)

        if self.request.GET:
            context['s_topic'] = self.request.GET.get('topic')
            context['s_created'] = self.request.GET.get('created')
            context['s_status'] = self.request.GET.get('status')
            context['s_theme'] = self.request.GET.get('theme')
            context['s_username'] = self.request.GET.get('username')

        return context


class TicketCreationView(LoginRequiredMixin, FormView):
    login_url = reverse_lazy("authapp:login")
    form_class = CreateTicketForm
    template_name = 'supportapp/create_ticket.html'
    success_url = reverse_lazy('support:tickets')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'].fields['user'].initial = self.request.user
        return context

    def form_valid(self, form):
        form.save()

        theme = form.cleaned_data['theme']
        ticket_init_message = form.cleaned_data['init_message']

        site = get_current_site(self.request)
        context = {
            "message": form.cleaned_data['init_message'],
            "protocol": ('https' if self.request.is_secure() else 'http'),
            "site_domain": site.domain,
            'site_name': site.name,
            'ticket_theme': theme,
            'ticket_init_message': ticket_init_message,
            'ticket_path': reverse_lazy('support:tickets')
        }

        message_body = render_to_string(
            template_name='supportapp/tech_support_ticket_start_email.html', context=context
        )

        send_mail(
            subject=f'Tech support: {theme if len(theme) < 20 else (theme[:25] + "...")}',
            message=message_body,
            from_email=settings.TECH_SUPPORT_EMAIL,
            recipient_list=[self.request.user.email, ],
            fail_silently=False,
        )

        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class CreateTicketMessageView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy("authapp:login")
    model = TicketMessage
    form_class = CreateTicketMessageForm

    def form_valid(self, form):
        self.object = form.save()
        rendered_message = render_to_string(
            template_name="supportapp/includes/message_card.html",
            context={"message": self.object, },
        )
        return JsonResponse({"card": rendered_message})


class TicketDetailView(UserPassesTestMixin, TemplateView):
    login_url = reverse_lazy("authapp:login")
    template_name = 'supportapp/ticket_chat.html'

    def test_func(self):
        is_owner = self.request.user == Ticket.objects.get(pk=self.kwargs["pk"]).user
        is_staff_or_admin = self.request.user.is_staff or self.request.user.is_superuser
        if is_owner or is_staff_or_admin:
            return True

    def get_context_data(self, pk=None, **kwargs):
        context = super().get_context_data(**kwargs)
        ticket = Ticket.objects\
            .select_related("user") \
            .prefetch_related(
            Prefetch(
                'messages',
                queryset=TicketMessage.objects.select_related('user')
                .only('user__id', 'user__username', 'user__is_staff',
                      'user__email', 'message', 'created', 'ticket_id')
            )) \
            .only('id', 'user__username', 'user__is_staff', 'user__email',
                  'init_message', 'status', 'topic', 'created', 'theme', 'attachment') \
            .filter(pk=pk).order_by('messages__created')

        ticket = ticket.first()
        context["ticket_data"] = ticket
        ticket_is_active = ticket.status == 1
        user_is_owner = context['ticket_data'].user.id == self.request.user.id
        user_is_staff_or_admin = self.request.user.is_staff or self.request.user.is_superuser
        if ticket_is_active and (user_is_owner or user_is_staff_or_admin):
            message_form = CreateTicketMessageForm(user=self.request.user, ticket=context['ticket_data'])
            status_form = TicketChangeStatusForm(user=self.request.user, ticket=context["ticket_data"])

            context["message_form"] = message_form
            context["status_form"] = status_form

        return context


class TicketChangeStatusView(UserPassesTestMixin, UpdateView):
    login_url = reverse_lazy("authapp:login")
    template_name = 'supportapp/ticket_status.html'
    model = Ticket
    form_class = TicketChangeStatusForm

    def test_func(self, *args, **kwargs):
        ticket = Ticket.objects.get(pk=self.kwargs['pk'])
        user_is_owner = ticket.user == self.request.user
        if user_is_owner or self.request.user.is_staff or self.request.user.is_superuser:
            return True

    def form_valid(self, form):
        form_status = form.cleaned_data.get("status")
        user_is_staff_or_super = self.request.user.is_staff or self.request.user.is_superuser
        form_status += user_is_staff_or_super + 1
        self.object.status = form_status
        self.object.save()
        return super().form_valid(form)
