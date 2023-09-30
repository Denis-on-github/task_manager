from django.contrib.auth.models import AbstractUser
from django.db import models


# In accordance with the assignment, the generated code needs to be commented
# FIXME: delete comments
# TODO: add admin settings for this models
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
