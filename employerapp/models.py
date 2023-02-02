from django.db import models

from ckeditor.fields import RichTextField
from django.db import models
from django.urls import reverse

from applicantapp.models import Towns, Skill
from authapp.models import CustomUser
from django.core.validators import RegexValidator

# Create your models here.

# # перечисление вида опыта работы (первичный ключ для "VacancyHeader")
# # Права доступа на редактирование: Модератор
# class WorkExperience(models.Model):
#     work_experience = models.CharField(max_length=1024, unique=True, verbose_name="Опыт работы")
#
#     def __str__(self) -> str:
#         return f"{self.work_experience}"
#
#     class Meta:
#         verbose_name = "Опыт работы"
#         verbose_name_plural = "Опыт работы"
#         ordering = ("work_experience",)


# # перечисление вида графика рабочего дня (первичный ключ для "VacancyHeader")
# # Права доступа на редактирование: Модератор
# class WorkingDay(models.Model):
#     working_day = models.CharField(max_length=256, unique=True, verbose_name="График рабочего дня")
#
#     def __str__(self) -> str:
#         return f"{self.working_day}"
#
#     class Meta:
#         verbose_name = "График работы"
#         verbose_name_plural = "График работы"
#         ordering = ("working_day",)


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
    cover = models.ImageField(upload_to="image/employment/", blank=True, verbose_name="Логотип организации")
    address = models.TextField(max_length=512, verbose_name="Адрес организации")
    # phone = models.CharField(max_length=256, verbose_name="Телефон организации")
    phoneNumberRegex = RegexValidator(regex=r"^\+?1?\d{8,15}$")
    phone = models.CharField(validators=[phoneNumberRegex], max_length=16, verbose_name="Телефон организации")
    email = models.EmailField(max_length=254, blank=True, verbose_name="email организации")
    website = models.URLField(max_length=200, blank=True, verbose_name="сайт организации")
    body = RichTextField(blank=True, verbose_name="Дополнительная информация")
    created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="Дата регистрации на портале")
    slug = models.SlugField(max_length=96, unique=True, db_index=True, verbose_name="URL префикс")
    location = models.TextField(max_length=1024, blank=True, verbose_name="Карта")
    # связь с таблицей базы applicantapp
    town_id = models.ForeignKey(Towns, on_delete=models.PROTECT, verbose_name="Местоположение")
    # связь с таблицей админки
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь')

    def get_absolute_url(self):
        return reverse('employerapp:employer_detail', kwargs={'employer_slug': self.slug})

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
    # work_experience_id = models.ForeignKey(WorkExperience, on_delete=models.PROTECT, verbose_name="Опыт работы")
    # working_day_id = models.ForeignKey(WorkingDay, on_delete=models.PROTECT, verbose_name="График рабочего дня")
    experience = models.PositiveSmallIntegerField(default=1, choices=EXPERIENCE, verbose_name="Опыт работы")
    employment_id = models.ManyToManyField(TypeEmployment, verbose_name="Вид занятости")
    town_id = models.ForeignKey(Towns, on_delete=models.PROTECT, verbose_name="Местоположение")
    skills_id = models.ManyToManyField(Skill, blank=True, verbose_name="Ключевой навык")
    employer_id = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name="vacancies", verbose_name="Работодатель")
    is_published = models.BooleanField(default=True, verbose_name="Опубликовать")

    def get_absolute_url(self):
        return reverse('employerapp:vacancy', kwargs={'vacancy_pk': self.pk})

    def __str__(self) -> str:
        return f"{self.job_title}"

    class Meta:
        verbose_name = "Вакансия"
        verbose_name_plural = "Вакансия"
        ordering = ("-created",)  # свежие в начале списка Длительность


# Перечисляемые разделы вакансии (дополнительная информация)
class VacancyBody(models.Model):
    title = models.CharField(max_length=256, verbose_name="Заголовок раздела вакансии")
    body = RichTextField(blank=True, null=True, verbose_name="Содержимое раздела вакансии")
    vacancy_header_id = models.ForeignKey(VacancyHeader, on_delete=models.CASCADE, verbose_name="Заголовок вакансии")
    ranking = models.PositiveSmallIntegerField(default=1, verbose_name="Очередность разделов")

    def __str__(self) -> str:
        return f"{self.title}"

    class Meta:
        verbose_name = "Детали вакансии"
        verbose_name_plural = "Детали вакансии"
        ordering = ("ranking",)


