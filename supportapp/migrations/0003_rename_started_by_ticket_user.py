# Generated by Django 4.1.5 on 2023-03-05 16:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("supportapp", "0002_fix_choices"),
    ]

    operations = [
        migrations.RenameField(
            model_name="ticket",
            old_name="started_by",
            new_name="user",
        ),
    ]