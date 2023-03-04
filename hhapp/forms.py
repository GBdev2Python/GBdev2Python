from django import forms
from django.core.exceptions import ValidationError
from django.conf import settings
from django.core.validators import RegexValidator


class FeedbackMailForm(forms.Form):
    user_id = forms.IntegerField(widget=forms.HiddenInput)
    message = forms.CharField(
        label='Сообщение',
        widget=forms.Textarea,
        validators=[
            RegexValidator(regex=settings.VALID_EMAIL_RE_PATTERN,
                           message='Сообщениe не может быть пустым, '
                                   'не может состоять только из цифр / специальных символов '
                                   'и должно содержать какой-то текст'),
        ]
    )

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields["user_id"].initial = user.pk
