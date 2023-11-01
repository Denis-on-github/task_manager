from django.contrib.auth.models import AbstractUser
from django.db import models
from main.services.storage_backends import public_storage


class User(AbstractUser):
    class Roles(models.TextChoices):
        DEVELOPER = "developer"
        MANAGER = "manager"
        ADMIN = "admin"

    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    username = models.CharField(max_length=50, blank=False, unique=True)
    role = models.CharField(
        max_length=255, choices=Roles.choices, default=Roles.DEVELOPER
    )
    email = models.EmailField(blank=False, unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True, unique=True)
    avatar_picture = models.ImageField(null=True, storage=public_storage)

    def __str__(self):
        return self.username
