from factory import Faker, SubFactory, PostGenerationMethodCall
from factory.django import DjangoModelFactory

from main.models import Tag, Task, User


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
        skip_postgeneration_save = True

    last_name = Faker("last_name")
    first_name = Faker("first_name")
    username = Faker("user_name")
    email = Faker("email")
    password = PostGenerationMethodCall("set_password", "password")


class TagFactory(DjangoModelFactory):
    class Meta:
        model = Tag

    title = Faker("word")


class TaskFactory(DjangoModelFactory):
    class Meta:
        model = Task

    title = Faker("sentence")
    description = Faker("paragraph")
    author = SubFactory(UserFactory)
    executor = SubFactory(UserFactory)
