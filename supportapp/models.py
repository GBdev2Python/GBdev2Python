from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class Ticket(models.Model):
    TICKET_TOPICS = (
        (1, "Registration"),
        (2, "Profile"),
        (3, "Login"),
        (4, "Account access"),
    )
    TICKET_STATUS = (
        (1, "active"),
        (2, "solved"),
        (3, "closed"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    init_message = models.TextField(verbose_name='Сообщение')
    topic = models.SmallIntegerField(verbose_name='Тема', choices=TICKET_TOPICS, default=1, blank=True)

    status = models.SmallIntegerField(choices=TICKET_STATUS, default=1, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'userid: {self.user_id} status: {self.TICKET_STATUS[self.status-1][1]} {self.TICKET_TOPICS[self.topic-1][1]}'

    def get_absolute_url(self):
        return reverse("support:ticket", kwargs={"pk": self.id})


class TicketMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, null=True, related_name='messages')

    message = models.CharField(verbose_name='Сообщение', max_length=255, blank=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user_id}: {self.message[:15]}...'

    class Meta:
        verbose_name = 'Messages'