import pytest

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from model_factories import TagFactory, UserFactory, TaskFactory


class TestPermissions(APITestCase):
    token_url = reverse("token_obtain_pair")

    def token_request(self, username: str = None, password: str = "password"):
        response = self.client.post(self.token_url, data={"username": username, "password": password})
        return response

    @pytest.mark.django_db
    def test_user_cannot_delete_task(self):
        tag = TagFactory.create()
        tag.save()

        user = UserFactory()
        user.save()

        task = TaskFactory.create(author=user, executor=user)
        task.save()
        task.tags.set([tag])

        response = self.token_request(username=user.username)
        token = response.json()["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.delete(f"/api/tasks/{task.id}/")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_user_cannot_delete_tag(self):
        tag = TagFactory.create()
        tag.save()

        user = UserFactory()
        user.save()

        response = self.token_request(username=user.username)
        token = response.json()["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.delete(f"/api/tags/{tag.id}/")
        assert response.status_code == status.HTTP_403_FORBIDDEN, response.content

    @pytest.mark.django_db
    def test_admin_can_delete_task(self):
        tag = TagFactory.create()
        tag.save()

        admin = UserFactory(is_staff=True)
        admin.save()

        task = TaskFactory.create(author=admin, executor=admin)
        task.save()
        task.tags.set([tag])

        response = self.token_request(username=admin.username)
        token = response.json()["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.delete(f"/api/tasks/{task.id}/")
        assert response.status_code == status.HTTP_204_NO_CONTENT

    @pytest.mark.django_db
    def test_admin_can_delete_tag(self):
        tag = TagFactory.create()
        tag.save()

        admin = UserFactory(is_staff=True)
        admin.save()

        response = self.token_request(username=admin.username)
        token = response.json()["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.delete(f"/api/tags/{tag.id}/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
