from datetime import datetime
from pathlib import Path

from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.validators import FileExtensionValidator

from .validators import file_size_validator


User = get_user_model()


def upload_directory_path(instance, filename):
    file_ext = Path(filename).suffix
    result_string = f'support/user_{instance.user.id}/{datetime.now()}{file_ext}'
    return result_string


class Ticket(models.Model):
    TICKET_TOPICS = (
        (1, "Регистрация"),
        (2, "Профиль"),
        (3, "Логин"),
        (4, "Доступ к аккаунту"),
    )
    TICKET_STATUS = (
        (1, "active"),
        (2, "solved"),
        (3, "closed"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    theme = models.CharField(
        verbose_name="Тема", max_length=100, blank=False,
        help_text="Тема не должна быть пустой и не может содержать большее чем 100 символов"
    )
    init_message = models.TextField(verbose_name='Сообщение', blank=False)
    topic = models.SmallIntegerField(verbose_name='Категория', choices=TICKET_TOPICS, default=1)
    attachment = models.FileField(
        verbose_name='Вложение',
        upload_to=upload_directory_path,
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(allowed_extensions=settings.SUPPORT_ALLOWED_FILE_FORMATS),
            file_size_validator],
        help_text=f"Вы можете приложить к обращению файлы следующих форматов: "
                  f"{', '.join(settings.SUPPORT_ALLOWED_FILE_FORMATS)}.\n"
                  f"Размер которых не превышает {settings.SUPPORT_MAX_FILE_SIZE // 1024 //1024} МБ"
    )

    status = models.SmallIntegerField(choices=TICKET_STATUS, default=1)
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