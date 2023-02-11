# Generated by Django 4.1.5 on 2023-02-06 19:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("applicantapp", "0002_initial"),
        ("employerapp", "__first__"),
    ]

    operations = [
        migrations.CreateModel(
            name="Response",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "cover_letter",
                    models.TextField(
                        blank=True, verbose_name="Сопроводительное письмо"
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("NEW", "Новая"),
                            ("READ", "Просмотрено"),
                            ("ACCEPTED", "Принято"),
                            ("REJECTED", "Отклонено"),
                        ],
                        default="NEW",
                        max_length=8,
                        verbose_name="Статус",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата публикации"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Обновлено"),
                ),
                (
                    "resume",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="applicantapp.resumes",
                        verbose_name="Резюме",
                    ),
                ),
                (
                    "vacancyheader",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="employerapp.vacancyheader",
                        verbose_name="Вакансии",
                    ),
                ),
            ],
            options={
                "verbose_name": "Отклик",
                "verbose_name_plural": "Отклики",
            },
        ),
    ]
