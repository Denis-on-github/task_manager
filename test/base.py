from http import HTTPStatus
from typing import List, Optional, Union

from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase

from main.models.user import User
from model_factories import UserFactory


class TestViewSetBase(APITestCase):
    user: User = None
    token_url = reverse("token_obtain_pair")
    client: APIClient = None
    basename: str
    user_attributes: dict

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.user = cls.create_api_user()
        cls.client = APIClient()

    def token_request(self, username: str = None, password: str = "password"):
        response = self.client.post(
            self.token_url, data={"username": username, "password": password}
        )
        return response

    @staticmethod
    def create_api_user():
        user_attributes = {
            "username": "g_tester",
            "first_name": "Good",
            "last_name": "Tester",
            "email": "tester@good-tests.com",
            "role": User.Roles.ADMIN.value,
            "is_staff": True,
            "is_active": True,
        }
        user = UserFactory.create(**user_attributes)
        user.save()
        return user

    @classmethod
    def detail_url(cls, key: Union[int, str]) -> str:
        return reverse(f"{cls.basename}-detail", args=[key])

    @classmethod
    def list_url(cls, args: List[Union[str, int]] = None) -> str:
        return reverse(f"{cls.basename}-list", args=args)

    def create(self, user_data: dict, args: List[Union[str, int]] = None) -> dict:
        response = self.token_request(username=self.user.username)
        token = response.json()["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.post(self.list_url(args), data=user_data)
        assert response.status_code == HTTPStatus.CREATED, response.content
        return response.data

    def request_create(self, user_data: dict, args: List[Union[str, int]] = None) -> dict:
        response = self.client.post(self.list_url(args), data=user_data)
        return response

    def list(self, filters: Optional[dict] = None) -> List[dict]:
        response = self.token_request(username=self.user.username)
        token = response.json()["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.get(self.list_url(), data=filters)
        assert response.status_code == HTTPStatus.OK, response.content
        return response.data

    def retrieve(self, pk: Union[str, int]) -> dict:
        response = self.token_request(username=self.user.username)
        token = response.json()["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.get(self.detail_url(pk))
        assert response.status_code == HTTPStatus.OK, response.content
        return response.data

    def update(self, pk: Union[str, int], data: dict) -> dict:
        response = self.token_request(username=self.user.username)
        token = response.json()["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.put(self.detail_url(pk), data=data)
        assert response.status_code == HTTPStatus.OK, response.content
        return response.data

    def delete(self, pk: Union[str, int]) -> None:
        response = self.client.delete(self.detail_url(pk))
        assert response.status_code == HTTPStatus.NO_CONTENT, response.content

    def request_single_resource(self, data: dict = None) -> Response:
        return self.client.get(self.list_url(), data=data)

    def single_resource(self, data: dict = None) -> dict:
        response = self.request_single_resource(data)
        assert response.status_code == HTTPStatus.OK
        return response.data

    def request_patch_single_resource(self, attributes: dict) -> Response:
        url = self.list_url()
        return self.client.patch(url, data=attributes)

    def patch_single_resource(self, attributes: dict) -> dict:
        response = self.request_patch_single_resource(attributes)
        assert response.status_code == HTTPStatus.OK, response.content
        return response.data
