from django.db import models

# Create your models here.


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

    class Meta:
        verbose_name = "Отклик"
        verbose_name_plural = "Отклики"
