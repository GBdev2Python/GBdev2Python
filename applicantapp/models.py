from django.db import models
from django.contrib.auth.models import User
from authapp.models import CustomUser
from django.urls import reverse
import uuid

# Create your models here.

# Справочник городов
class Towns(models.Model):
    town = models.CharField(max_length=50, unique=True, db_index=True, verbose_name="Город")
   # id = models.UUIDField(default=uuid.uuid4, unique=True,
    #                      primary_key=True, editable=False)
    def __str__(self) -> str:
        return f"{self.town}"

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"
        ordering = ("town",)


# Соискатель (Таблица хранения данных по соискателям)
class Applicants(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Пользователь')
    image = models.ImageField(null=True, blank=True, upload_to='image/applicant', default="image/applicant/default.jpg")
    birthday = models.DateField(blank=True, verbose_name="Дата рождения")
    phone = models.CharField(max_length=20, verbose_name="Телефон соискателя")
    town = models.ForeignKey(Towns, on_delete=models.PROTECT, verbose_name="Город проживания")
   # id = models.UUIDField(default=uuid.uuid4, unique=True,
    #                      primary_key=True, editable=False)

    def __str__(self) -> str:
        return f"{self.user.first_name} {self.user.last_name}"


    def get_absolute_url(self):
        return reverse ('applicant_by_id',kwargs = {'applicant_id':self.id})


    class Meta:
        verbose_name = "Соискатель"
        verbose_name_plural = "Соискатели"


# Ключевые навыки соискателей

class Skill(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True, verbose_name="Навык")
    # description = models.TextField(null=True, blank=True, verbose_name='Описание навыка')
    # а зачем записывать дату создания навыка?
   # created = models.DateTimeField(auto_now_add=True)
   # id = models.UUIDField(default=uuid.uuid4, unique=True,
    #                      primary_key=True, editable=False)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "Навык"
        verbose_name_plural = "Навыки"



class Resumes(models.Model):
    applicants = models.ForeignKey(Applicants,on_delete=models.CASCADE, verbose_name='Соискатель')
    verification = models.BooleanField(default=False,blank=False, verbose_name='Прохождение модерации')
    required_job = models.TextField(blank=True, null=True, verbose_name='Требуемая работа/должность')
    image = models.ImageField(null=True, blank=True, upload_to='applicant_images', default="applicant_images/default.jpg", verbose_name="FOTO")
    skills = models.ManyToManyField(Skill, blank=True,verbose_name='Ключевые навыки')
    salary = models.CharField(max_length=30, blank=True, null=True, verbose_name='Зарплата')
    last_job = models.TextField(null=True, blank=True, verbose_name='Последнее место работы')
    education = models.TextField(null=True, blank=True, verbose_name='Образование/курсы')
    created = models.DateTimeField(auto_now_add=True,verbose_name='Дата создания резюме')
    is_published = models.BooleanField(default=False, verbose_name="Опубликовать")
   # id = models.UUIDField(default=uuid.uuid4, unique=True,
    #                      primary_key=True, editable=False)

    def __str__(self):
        return str(f'{self.applicants.user.first_name} {self.id}')


    def get_absolute_url(self):
        return reverse ('resume_by_id',kwargs = {'resume_id':self.id})


    class Meta:
        verbose_name = "Резюме"
        verbose_name_plural = "Резюме"
