# Create your models here.

from ckeditor.fields import RichTextField
from django.db import models
from django.urls import reverse


# Create your models here.

# перечисление городов, округов (первичный ключ для "VacancyHeader" + сущности "Соискатель")
# Права доступа на редактирование: Модератор
class Locality(models.Model):
    town = models.CharField(max_length=256, unique=True, db_index=True, verbose_name="Местоположение")

    def __str__(self) -> str:
        return f"{self.town}"

    class Meta:
        verbose_name = "Местоположение"
        verbose_name_plural = "Местоположение"
        ordering = ("town",)


# перечисление вида опыта работы (первичный ключ для "VacancyHeader")
# Права доступа на редактирование: Модератор
class WorkExperience(models.Model):
    work_experience = models.CharField(max_length=1024, unique=True, verbose_name="Опыт работы")

    def __str__(self) -> str:
        return f"{self.work_experience}"

    class Meta:
        verbose_name = "Опыт работы"
        verbose_name_plural = "Опыт работы"
        ordering = ("work_experience",)


# перечисление вида графика рабочего дня (первичный ключ для "VacancyHeader")
# Права доступа на редактирование: Модератор
class WorkingDay(models.Model):
    working_day = models.CharField(max_length=256, unique=True, verbose_name="Длительность рабочего дня")

    def __str__(self) -> str:
        return f"{self.working_day}"

    class Meta:
        verbose_name = "Длительность рабочего дня"
        verbose_name_plural = "Длительность рабочего дня"
        ordering = ("working_day",)


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
    phone = models.CharField(max_length=256, verbose_name="Телефон организации")
    email = models.EmailField(max_length=254, blank=True, verbose_name="email организации")
    website = models.URLField(max_length=200, blank=True, verbose_name="сайт организации")
    body = RichTextField(blank=True, null=True, verbose_name="Дополнительная информация")
    created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="Дата регистрации на портале")
    slug = models.SlugField(max_length=128, unique=True, db_index=True, verbose_name="URL префикс")
    town_id = models.ForeignKey(Locality, on_delete=models.PROTECT, verbose_name="Местоположение")

    def get_absolute_url(self):
        return reverse('employer_detail', kwargs={'employer_slug': self.slug})

    def __str__(self) -> str:
        return f"{self.employment}"

    class Meta:
        verbose_name = "Работодатель"
        verbose_name_plural = "Работодатель"


# Вакансия работодателя
class VacancyHeader(models.Model):
    job_title = models.CharField(max_length=256, verbose_name="Название вакансии")
    salary = models.PositiveIntegerField(default=0, verbose_name="Заработная плата")
    created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="Дата создания")
    work_experience_id = models.ForeignKey(WorkExperience, on_delete=models.PROTECT, verbose_name="Опыт работы")
    working_day_id = models.ForeignKey(WorkingDay, on_delete=models.PROTECT, verbose_name="График рабочего дня")
    employment_id = models.ForeignKey(TypeEmployment, on_delete=models.PROTECT, verbose_name="Вид занятости")
    town_id = models.ForeignKey(Locality, on_delete=models.PROTECT, verbose_name="Местоположение")
    employer_id = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name="vacancies", verbose_name="Работодатель")
    is_published = models.BooleanField(default=True, verbose_name="Опубликовать")

    def get_absolute_url(self):
        return reverse('vacancy', kwargs={'vacancy_pk': self.pk})

    def __str__(self) -> str:
        return f"{self.job_title}"

    class Meta:
        verbose_name = "Вакансия"
        verbose_name_plural = "Вакансия"
        ordering = ("-created",)  # свежие в начале списка


# Перечисляемые разделы вакансии (дополнительная информация)
class VacancyBody(models.Model):
    title = models.CharField(max_length=256, verbose_name="Заголовок раздела вакансии")
    body = RichTextField(blank=True, null=True, verbose_name="Содержимое раздела вакансии")
    vacancy_header_id = models.ForeignKey(VacancyHeader, on_delete=models.CASCADE, verbose_name="Заголовок вакансии")

    def __str__(self) -> str:
        return f"{self.title}"

    class Meta:
        verbose_name = "Детали вакансии"
        verbose_name_plural = "Детали вакансии"


