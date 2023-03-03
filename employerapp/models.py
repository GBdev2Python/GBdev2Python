from ckeditor.fields import RichTextField
from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse

from applicantapp.models import Skill, Towns
from authapp.models import CustomUser

# Create your models here.

# перечисление вида занятости (первичный ключ для "VacancyHeader")
# Права доступа на редактирование: Модератор


class TypeEmployment(models.Model):
    employment = models.CharField(max_length=256, unique=True, verbose_name="Вид занятости")

    def __str__(self) -> str:
        return f"{self.employment}"

    class Meta:
        verbose_name = "Вид занятости"
        verbose_name_plural = "Вид занятости"
        ordering = ("employment",)


# Работодатель (Общий реестр по всем работодателям)
# первичный ключ для "VacancyHeader"
class Employer(models.Model):
    employment = models.TextField(max_length=1024, verbose_name="Работодатель")
    cover = models.ImageField(upload_to="employment/", blank=True, default="employment/logo_default.jpg", verbose_name="Логотип организации")
    address = models.TextField(max_length=512, verbose_name="Адрес организации")
    # phone = models.CharField(max_length=256, verbose_name="Телефон организации")
    # phoneNumberRegex = RegexValidator(regex=r"^\+?1?\d{8,15}$")
    phoneNumberRegex = RegexValidator(regex=r"^\d{8,12}$")
    phone = models.CharField(validators=[phoneNumberRegex], max_length=12, verbose_name="Телефон организации")
    email = models.EmailField(max_length=254, blank=True, verbose_name="email организации")
    website = models.URLField(max_length=200, blank=True, verbose_name="сайт организации")
    body = RichTextField(blank=True, verbose_name="Дополнительная информация")
    created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="Дата регистрации на портале")
    location = models.TextField(max_length=1024, blank=True, verbose_name="Карта")
    # связь с таблицей базы applicantapp
    town_id = models.ForeignKey(Towns, on_delete=models.PROTECT, verbose_name="Местоположение")
    # связь с таблицей админки
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, verbose_name="Пользователь")

    def get_absolute_url(self):
        return reverse("employerapp:employer_detail", kwargs={"employer_id": self.pk})

    def __str__(self) -> str:
        return f"{self.employment}"

    class Meta:
        verbose_name = "Работодатель"
        verbose_name_plural = "Работодатель"


# Вакансия работодателя
class VacancyHeader(models.Model):
    EXPERIENCE = [
        (1, "не требуется"),
        (2, "не менее года"),
        (3, "1–3 года"),
        (4, "3–6 лет"),
    ]
    job_title = models.CharField(max_length=256, verbose_name="Название вакансии")
    salary = models.PositiveIntegerField(default=0, verbose_name="Заработная плата")
    created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="Дата создания")
    experience = models.PositiveSmallIntegerField(default=1, choices=EXPERIENCE, verbose_name="Опыт работы")
    body = RichTextField(blank=True, verbose_name="Содержимое раздела вакансии")
    is_published = models.BooleanField(default=True, verbose_name="Опубликовать")
    employment_id = models.ManyToManyField(TypeEmployment, verbose_name="Вид занятости")
    town_id = models.ForeignKey(Towns, on_delete=models.PROTECT, verbose_name="Местоположение")
    skills_id = models.ManyToManyField(Skill, blank=True, verbose_name="Ключевой навык")
    employer_id = models.ForeignKey(
        Employer, on_delete=models.CASCADE, related_name="vacancies", verbose_name="Работодатель"
    )

    def get_absolute_url(self):
        return reverse("employerapp:vacancy", kwargs={"vacancy_pk": self.pk})

    def __str__(self) -> str:
        return f"{self.job_title}"

    class Meta:
        verbose_name = "Вакансия"
        verbose_name_plural = "Вакансия"
        ordering = ("-created",)  # свежие в начале списка Длительность
