import pytest

from rest_framework import status
from rest_framework.test import APITestCase

from model_factories import TagFactory, UserFactory, TaskFactory


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
