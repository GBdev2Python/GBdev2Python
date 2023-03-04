from django.test import TestCase, Client
from django.core import mail
from django.conf import settings
from django.urls import reverse

from authapp.models import CustomUser
from hhapp.forms import FeedbackMailForm


class TestEmailSent(TestCase):
    fixtures = (
        'authapp/fixtures/001_test_user.json',
    )

    def setUp(self) -> None:
        self.test_cases = (
            ('123123123', False),
            ('!&@*#(!(!@#(#(#112312312!\n12333123123\nadasdasd', True),
            ('dhajaskskd11', True),
            ('HELLOW!*!@(#DNUGAUAUSJ!!', True),
            ('asd123asd123!&@*#asd', True),
            ('123123123*!()!)@#*!@#(!@#\n\n\n\n\t\t\t1233129310@*(!(!', False),
            ('a123123a', False),
            ('as123123as,', False),
            ('as123123asd,', True),
            ('', False),
            ('     ', False),
            ('екст', True),
            ("ТЕКСТФ*!(!(!(ФОФО128293", True)
        )

        self.client_with_auth = Client()
        login_url = reverse('authapp:login')
        self.client_with_auth.post(login_url, data={"username": "admin@post.com", 'password': '1111qqqqa'})

        self.message_form = FeedbackMailForm

    def test_mail_content_verified(self):
        user = CustomUser.objects.first()

        for message, result in self.test_cases:
            mail.send_mail(
                settings.TECH_SUPPORT_EMAIL_SUBJECT.replace('%user', user.email),
                message=message,
                from_email=user.email,
                recipient_list=[settings.TECH_SUPPORT_EMAIL, ],
                fail_silently=False,
            )

            f = self.message_form(data={'user_id': user.id, 'message': message})
            self.assertEqual(f.is_valid(), result, f'Message:'
                                                   f'\n{message} expected to be {result},'
                                                   f'\n got {f.is_valid()} instead')

        mails_sent = len(mail.outbox)
        self.assertEqual(mails_sent, 13, f'13 emails must be sent, got {mails_sent}')
