from django.core.exceptions import ValidationError
from django.conf import settings


def file_size_validator(value):
    limit = settings.SUPPORT_MAX_FILE_SIZE
    if value.size > limit:
        raise ValidationError("Файл слишком большой, "
                              "разрешенный размер не более 5 МБ. Пожалуйста выберите другйо файл")
