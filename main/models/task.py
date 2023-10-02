from django.db import models

from main.models import User
from main.models.tag import Tag


# In accordance with the assignment, the generated code needs to be commented
# FIXME: delete comments
# TODO: add admin settings for this models
class Task(models.Model):
    class TaskStatus(models.TextChoices):
        NEW_TASK = "new task"
        IN_DEVELOPMENT = "in development"
        IN_QA = "in qa"
        IN_CODE_REVIEW = "in code review"
        READY_FOR_RELEASE = "ready_for_release"
        RELEASED = "released"
        ARCHIVED = "archived"

    title = models.CharField(max_length=255)
    description = models.TextField()
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    due_date = models.DateTimeField()
    status = models.CharField(
        max_length=20, choices=TaskStatus.choices, default=TaskStatus.NEW_TASK
    )
    priority = models.IntegerField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="authored_tasks"
    )
    executor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="executed_tasks"
    )
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title
