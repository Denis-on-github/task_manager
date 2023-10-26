from http import HTTPStatus
from typing import List, Optional, Union

from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase

from main.models.user import User


class TestViewSetBase(APITestCase):
    user: User = None
    client: APIClient = None
    basename: str
    user_attributes: dict

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.user = cls.create_api_user()
        print(f"=== Tester (admin) created: {cls.user} ===")
        cls.client = APIClient()

    @staticmethod
    def create_api_user():
        user_attributes = {
            "username": "g_tester",
            "first_name": "Good",
            "last_name": "Tester",
            "email": "tester@good-tests.com",
            "role": User.Roles.ADMIN.value,
            "is_staff": True,
        }
        user = User.objects.create(**user_attributes)
        return user

    @classmethod
    def detail_url(cls, key: Union[int, str]) -> str:
        return reverse(f"{cls.basename}-detail", args=[key])

    @classmethod
    def list_url(cls, args: List[Union[str, int]] = None) -> str:
        return reverse(f"{cls.basename}-list", args=args)

    def create(self, data: dict, args: List[Union[str, int]] = None) -> dict:
        self.client.force_login(self.user)
        response = self.client.post(self.list_url(args), data=data)
        assert response.status_code == HTTPStatus.CREATED, response.content
        return response.data

    def list(self, filters: Optional[dict] = None) -> List[dict]:
        self.client.force_login(self.user)
        response = self.client.get(self.list_url(), data=filters)
        assert response.status_code == HTTPStatus.OK, response.content
        return response.data

    def retrieve(self, pk: Union[str, int]) -> dict:
        self.client.force_login(self.user)
        response = self.client.get(self.detail_url(pk))
        assert response.status_code == HTTPStatus.OK, response.content
        return response.data

    def update(self, pk: Union[str, int], data: dict) -> dict:
        self.client.force_login(self.user)
        response = self.client.put(self.detail_url(pk), data=data)
        assert response.status_code == HTTPStatus.OK, response.content
        return response.data

    def delete(self, pk: Union[str, int]) -> None:
        response = self.client.delete(self.detail_url(pk))
        assert response.status_code == HTTPStatus.NO_CONTENT, response.content
