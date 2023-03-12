from django.db import models
from django.urls import reverse

from authapp.models import CustomUser


class Towns(models.Model):
    town = models.CharField(max_length=50, unique=True, db_index=True, verbose_name="Город")

    def __str__(self) -> str:
        return f"{self.town}"

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"
        ordering = ("town",)


class Applicants(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Пользователь"
    )
    first_name = models.CharField(max_length=150, blank=True, verbose_name="Имя")
    last_name = models.CharField(max_length=150, blank=True, verbose_name="Фамилия")
    image = models.ImageField(null=True, blank=True, upload_to="image/applicant", default="image/applicant/default.jpg")
    birthday = models.DateField(blank=True, verbose_name="Дата рождения")
    phone = models.CharField(max_length=20, verbose_name="Телефон соискателя")
    town = models.ForeignKey(Towns, on_delete=models.PROTECT, verbose_name="Город проживания")

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):
        return reverse("applicant_by_id", kwargs={"applicant_id": self.id})

    class Meta:
        verbose_name = "Соискатель"
        verbose_name_plural = "Соискатели"


class Skill(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True, verbose_name="Навык")

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "Навык"
        verbose_name_plural = "Навыки"


class Resumes(models.Model):
    applicants = models.ForeignKey(Applicants, null=True, blank=True, on_delete=models.CASCADE,
                                   verbose_name="Соискатель")
    verification = models.BooleanField(default=False, blank=True, verbose_name="Прохождение модерации")
    required_job = models.TextField(blank=True, null=True, verbose_name="Требуемая работа/должность")
    image = models.ImageField(null=True, blank=True, upload_to="applicant_images", default="image/applicant/default.jpg", verbose_name="FOTO")
    skills = models.ManyToManyField(Skill, blank=True, verbose_name="Ключевые навыки")
    salary = models.CharField(max_length=30, blank=True, null=True, verbose_name="Зарплата")
    town_job = models.ForeignKey(Towns, on_delete=models.PROTECT, verbose_name="Поиск работы в городе:")
    last_job = models.TextField(null=True, blank=True, verbose_name="Последнее место работы")
    education = models.TextField(null=True, blank=True, verbose_name="Образование/курсы")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания резюме")
    is_published = models.BooleanField(blank=True, default=False, verbose_name="Опубликовать")

    def __str__(self):
        return str(f"{self.applicants.first_name} {self.required_job}")

    def get_absolute_url(self):
        return reverse("applicant:resume_by_id", kwargs={"resume_id": self.id})

    class Meta:
        verbose_name = "Резюме"
        verbose_name_plural = "Резюме"


class ResumeInvitation(models.Model):
    INVITATION_STATUS = (
        (1, "Ожидание"),
        (2, "Принято"),
        (2, "Отклонено"),
    )

    resume = models.ForeignKey(Resumes, on_delete=models.CASCADE)
    vacancy = models.ForeignKey('employerapp.VacancyHeader', on_delete=models.CASCADE,
                                verbose_name="Ваши вакансии")

    cover_letter = models.TextField(verbose_name="Дополнительная информация для пользователя")
    status = models.SmallIntegerField(verbose_name='Статус приглашения', choices=INVITATION_STATUS, default=1)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Приглашение'
        verbose_name_plural = 'Приглашения'

    def __str__(self):
        return f'{self.id} {self.resume if hasattr(self, "resume") else "NoRes"}'

    # @classmethod
    # def _get_self_vacancies(cls):
    #     return True