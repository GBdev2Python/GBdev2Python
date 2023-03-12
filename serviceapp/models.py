from django.db import models
from django.urls import reverse


class Response(models.Model):
    STATUS_CHOICES = [
        ("NEW", "Новая"),
        ("READ", "Просмотрено"),
        ("ACCEPTED", "Принято"),
        ("REJECTED", "Отклонено"),
    ]
    cover_letter = models.TextField(blank=True, verbose_name="Сопроводительное письмо")
    resume = models.ForeignKey("applicantapp.Resumes", on_delete=models.PROTECT, null=True, verbose_name="Резюме")
    vacancyheader = models.ForeignKey(
        "employerapp.VacancyHeader", on_delete=models.PROTECT, null=True, verbose_name="Вакансии"
    )
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default="NEW", verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")

    def get_absolute_url(self):
        return reverse("serviceapp:response_view", kwargs={"response_id": self.id})

    class Meta:
        verbose_name = "Отклик"
        verbose_name_plural = "Отклики"
