import pytest

from factory import Factory, Faker, SubFactory
from rest_framework import status
from rest_framework.test import APITestCase

from main.models import Tag, Task, User


class UserFactory(Factory):
    class Meta:
        model = User

    last_name = Faker("last_name")
    first_name = Faker("first_name")
    email = Faker("email")
    password = Faker("password")


class TagFactory(Factory):
    class Meta:
        model = Tag

    title = Faker("word")


class TaskFactory(Factory):
    class Meta:
        model = Task

    title = Faker("sentence")
    description = Faker("paragraph")
    author = SubFactory(UserFactory)
    executor = SubFactory(UserFactory)


class TestPermissions(APITestCase):
    @pytest.mark.django_db
    def test_user_cannot_delete_task(self):
        tag = TagFactory.create()
        tag.save()
        print(f"\n=== Tag for task created: {tag} ===")

        user = UserFactory()
        user.save()
        print(f"\n=== User for task created: {user} ===")

        task = TaskFactory.create(author=user, executor=user)
        task.save()
        task.tags.set([tag])
        print(f"\n=== Task created: {task} ===")

        self.client.force_login(user)

        response = self.client.delete(f"/api/tasks/{task.id}/")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_user_cannot_delete_tag(self):
        tag = TagFactory.create()
        tag.save()
        print(f"\n=== Tag created: {tag} ===")

        user = UserFactory()
        user.save()
        print(f"\n=== User created: {user} ===")

        self.client.force_login(user)

        response = self.client.delete(f"/api/tags/{tag.id}/")
        assert response.status_code == status.HTTP_403_FORBIDDEN, response.content

    @pytest.mark.django_db
    def test_admin_can_delete_task(self):
        tag = TagFactory.create()
        tag.save()
        print(f"\n=== Tag for task created: {tag} ===")

        admin = UserFactory(is_staff=True)
        admin.save()
        print(f"\n=== Admin for task created: {admin} ===")

        task = TaskFactory.create(author=admin, executor=admin)
        task.save()
        task.tags.set([tag])
        print(f"\n=== Task created: {task} ===")

        self.client.force_login(admin)

        response = self.client.delete(f"/api/tasks/{task.id}/")
        assert response.status_code == status.HTTP_204_NO_CONTENT

    @pytest.mark.django_db
    def test_admin_can_delete_tag(self):
        tag = TagFactory.create()
        tag.save()
        print(f"\n=== Tag created: {tag} ===")

        admin = UserFactory(is_staff=True)
        admin.save()
        print(f"\n=== Admin for task created: {admin} ===")

        self.client.force_login(admin)

        response = self.client.delete(f"/api/tags/{tag.id}/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
