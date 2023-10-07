from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Roles(models.TextChoices):
        DEVELOPER = "developer"
        MANAGER = "manager"
        ADMIN = "admin"

    last_name = models.CharField(max_length=50, blank=False)
    first_name = models.CharField(max_length=50, blank=False)
    role = models.CharField(
        max_length=255, choices=Roles.choices, default=Roles.DEVELOPER
    )
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.last_name
