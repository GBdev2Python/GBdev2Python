from django import forms
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
    topic = forms.CharField(max_length=100, label="Тема")

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields["user_id"].initial = user.pk
            self.fields["topic"].initial = settings.TECH_SUPPORT_EMAIL_SUBJECT.replace('%user', user.email)

    field_order = ['topic', 'message']
