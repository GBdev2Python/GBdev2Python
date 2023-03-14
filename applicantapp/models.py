from django.db import models
from django.urls import reverse

from authapp.models import CustomUser


class Towns(models.Model):
    town = models.CharField(max_length=50, unique=True, db_index=True, verbose_name="Город")

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"
        ordering = ("town",)

    def __str__(self) -> str:
        return f"{self.town}"


class Applicants(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Пользователь"
    )
    first_name = models.CharField(max_length=150, blank=True, verbose_name="Имя")
    last_name = models.CharField(max_length=150, blank=True, verbose_name="Фамилия")
    image = models.ImageField(
        null=True, blank=True, upload_to="image/applicant", default="image/applicant/default.jpg"
    )
    birthday = models.DateField(blank=True, verbose_name="Дата рождения")
    phone = models.CharField(max_length=20, verbose_name="Телефон соискателя")
    town = models.ForeignKey(Towns, on_delete=models.PROTECT, verbose_name="Город проживания")

    class Meta:
        verbose_name = "Соискатель"
        verbose_name_plural = "Соискатели"

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):
        return reverse("applicant_by_id", kwargs={"applicant_id": self.id})


class Skill(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True, verbose_name="Навык")

    class Meta:
        verbose_name = "Навык"
        verbose_name_plural = "Навыки"

    def __str__(self):
        return str(self.name)


class Resumes(models.Model):
    applicants = models.ForeignKey(Applicants, null=True, blank=True, on_delete=models.CASCADE,
                                   verbose_name="Соискатель")
    verification = models.BooleanField(default=False, blank=True, verbose_name="Прохождение модерации")
    required_job = models.TextField(blank=True, null=True, verbose_name="Требуемая работа/должность")
    image = models.ImageField(
        null=True, blank=True, upload_to="applicant_images",
        default="image/applicant/default.jpg", verbose_name="Фотография"
    )
    skills = models.ManyToManyField(Skill, blank=True, verbose_name="Ключевые навыки")
    salary = models.PositiveIntegerField(default=0, verbose_name="Зарплата")
    town_job = models.ForeignKey(Towns, on_delete=models.PROTECT, verbose_name="Поиск работы в городе:")
    education = models.TextField(null=True, blank=True, verbose_name="Образование/курсы")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания резюме")
    is_published = models.BooleanField(blank=True, default=False, verbose_name="Опубликовать")

    class Meta:
        verbose_name = "Резюме"
        verbose_name_plural = "Резюме"

    def __str__(self):
        return str(f"{self.applicants.first_name} {self.required_job}")

    def get_absolute_url(self):
        return reverse("applicant:resume_by_id", kwargs={"resume_id": self.id})


class Experience(models.Model):
    resume = models.ForeignKey(Resumes, verbose_name='', on_delete=models.CASCADE, related_name='experience')

    company = models.CharField(max_length=128, verbose_name='Компания')
    description = models.TextField(verbose_name='Ваши достижения', blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.pk} c:{self.company[:5]} d:{self.description[:5]}'


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
