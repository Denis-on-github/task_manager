from unittest.mock import patch, MagicMock

from django.core import mail
from django.template.loader import render_to_string

from main.models import Task
from services.emails import send_assign_notification
from base import TestViewSetBase
from model_factories import UserFactory, TaskFactory
from task_manager.settings import DEFAULT_FROM_EMAIL


class TestSendEmail(TestViewSetBase):
    @patch.object(mail, "send_mail")
    def test_send_assign_notification(self, fake_sender: MagicMock) -> None:
        assignee = UserFactory.create()
        task = TaskFactory.create(author=assignee)

        send_assign_notification(task.id)

        fake_sender.assert_called_once_with(
            subject="You've assigned a task.",
            message="",
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=[assignee.email],
            html_message=render_to_string(
                "emails/notification.html",
                context={"task": Task.objects.get(pk=task.id)},
            ),
        )
