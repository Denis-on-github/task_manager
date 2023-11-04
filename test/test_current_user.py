import os
from urllib.parse import urlparse

from base import TestViewSetBase


class TestUserViewSet(TestViewSetBase):
    basename = "current_user"

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()

    def test_retrieve(self):
        user = self.single_resource()
        user['avatar_picture'] = os.path.basename(urlparse(user['avatar_picture']).path)

        assert user == {
            'id': self.user.id,
            'email': self.user.email,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'role': self.user.role,
            'username': self.user.username,
            'avatar_picture': str(self.user.avatar_picture)
        }

    def test_patch(self):
        # self.token_request(username=self.user.username)
        self.patch_single_resource({"first_name": "TestName"})

        user = self.single_resource()
        assert user["first_name"] == "TestName"
