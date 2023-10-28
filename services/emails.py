from typing import Optional

from django.core import mail
from django.template.loader import render_to_string

from main.models import Task
from task_manager.settings import DEFAULT_FROM_EMAIL


def send_assign_notification(task_id: int) -> None:
    task = Task.objects.get(pk=task_id)
    assignee = task.author
    send_html_email(
        subject="You've assigned a task.",
        template="notification.html",
        context={"task": task},
        recipients=[assignee.email],
    )


def send_html_email(
    subject: str,
    template: str,
    context: dict,
    recipients: list[str],
    message: Optional[str] = "",
    from_email: Optional[str] = DEFAULT_FROM_EMAIL,
) -> None:
    html_message = render_to_string(f"emails/{template}", context)
    return mail.send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=recipients,
        html_message=html_message,
    )
