from http import HTTPStatus
from pathlib import Path

from django.core import mail
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.conf import settings

from supportapp.models import Ticket, TicketMessage


User = get_user_model()


class TicketMessagesTest(TestCase):
    fixtures = (
        'employerapp/fixtures/001_customuser.json',
        'supportapp/fixtures/011_test_tickets.json',
    )

    def setUp(self) -> None:
        super().setUp()
        self.client_with_auth = Client()
        self.client_with_auth_no_staff = Client()
        login_url = reverse("authapp:login")
        self.client_with_auth.post(path=login_url, data={"username": 'admin', "password": '1111qqqqa'})
        self.client_with_auth_no_staff.post(path=login_url, data={"username": "employer2", "password": '1111qqqa'})

        self.routes = {
            "create": {
                "ticket": reverse("support:create_ticket"),
                "message": reverse("support:create_message"),
            },
            "get": {
                "ticket": reverse("support:tickets"),
            }
        }

    def test_open_support_authed(self):
        response = self.client_with_auth.get(path=self.routes['get']['ticket'])
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_open_support_no_auth(self):
        response = self.client.get(path=self.routes['get']['ticket'])
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_create_ticket_authed(self):
        total_tickets = Ticket.objects.count()
        ticket_data = {"init_message": "Test_ticket", "theme": "Test_theme", "user": 1, "topic": 1}

        self.client_with_auth.post(path=self.routes['create']['ticket'], data=ticket_data)
        self.assertEqual(Ticket.objects.count(), total_tickets + 1)

        test_ticket = Ticket(user_id=1, init_message="Test_ticket", theme="Test_theme", topic=1, status=1)
        last_ticket = Ticket.objects.last()

        self.assertTrue(
            all((test_ticket.user == last_ticket.user,
                 test_ticket.theme == last_ticket.theme,
                 test_ticket.init_message == last_ticket.init_message,
                 test_ticket.topic == last_ticket.topic,
                 test_ticket.status == last_ticket.status,
                 ))
        )

    def test_post_image_in_form(self):
        file_path = Path(__file__).parent
        total_tickets = Ticket.objects.count()

        with open(file_path / 'test_file.txt', 'rb') as f:
            ticket_data = {"init_message": "Test_ticket", "theme": "Test_theme", "user": 1, "topic": 1, 'attachment': f}
            self.client_with_auth.post(path=self.routes['create']['ticket'], data=ticket_data)

        self.assertEqual(total_tickets + 1, Ticket.objects.count())
        self.assertEqual(len(mail.outbox), 1)

    def test_create_ticket_no_auth(self):
        total_tickets = Ticket.objects.count()
        ticket_data = {"init_message": "Test_ticket", "theme": "Test_theme", "user": 1}
        self.client.post(path=self.routes['create']['ticket'], data=ticket_data)
        self.assertEqual(total_tickets, Ticket.objects.count())

    def test_create_ticket_message_created_authed(self):
        total_messages = TicketMessage.objects.count()
        message_data = {"user": 1, "ticket": 1, "message": "test_message_1"}
        self.client_with_auth.post(self.routes['create']['message'], data=message_data)
        self.assertEqual(TicketMessage.objects.count(), total_messages + 1)

        test_message = TicketMessage(user_id=1, ticket_id=1, message="test_message_1")
        last_message = TicketMessage.objects.last()

        self.assertTrue(
            all((test_message.user == last_message.user,
                 test_message.ticket == last_message.ticket,
                 test_message.message == last_message.message,
                 ))
        )

    def test_create_ticket_message_created_no_auth(self):
        total_messages = TicketMessage.objects.count()
        message_data = {"user": 1, "ticket": 1, "message": "test_message_1"}

        self.client.post(self.routes['create']['message'], data=message_data)
        self.assertEqual(TicketMessage.objects.count(), total_messages)

    def test_open_ticket_owner(self):
        ticket_url = reverse("support:ticket", args=(1, ))
        response = self.client_with_auth.get(ticket_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_open_ticket_not_owner_but_staff(self):
        ticket_url = reverse("support:ticket", args=(3, ))
        response = self.client_with_auth.get(ticket_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_open_ticket_not_owner_not_staff(self):
        ticket_url = reverse("support:ticket", args=(2,))
        response = self.client_with_auth_no_staff.get(ticket_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
