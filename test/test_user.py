from base import TestViewSetBase

from main.models import User


class TestUserViewSet(TestViewSetBase):
    basename = "users"
    user_attributes = {
        "first_name": "test",
        "last_name": "user",
        "username": "test_user",
        "email": "test_user@test-email.com",
        "role": User.Roles.DEVELOPER.value,
    }

    def setUp(self):
        super().setUp()
        self.test_user = self.create(self.user_attributes)

    @staticmethod
    def expected_details(entity: dict, attributes: dict):
        return {**attributes, "id": entity["id"]}

    def test_create(self):
        expected_response = self.expected_details(self.test_user, self.user_attributes)
        assert self.test_user == expected_response

    def test_list(self):
        expected_response = self.expected_details(self.test_user, self.user_attributes)
        user_list = self.list()
        assert expected_response in user_list

    def test_retrieve(self):
        retrieved_user = self.retrieve(self.test_user["id"])
        expected_response = self.expected_details(self.test_user, self.user_attributes)
        assert retrieved_user == expected_response

    def test_update(self):
        updated_attributes = {
            "first_name": "updated_user",
            "last_name": "updated_test",
            "username": "updated_user",
            "email": "updated_test_user@test-email.com",
            "role": User.Roles.MANAGER.value,
        }
        updated_user = self.update(self.test_user["id"], updated_attributes)
        expected_response = self.expected_details(updated_user, updated_attributes)
        assert updated_user == expected_response

    def test_delete(self):
        self.delete(self.test_user["id"])
        try:
            self.retrieve(self.test_user["id"])
        except AssertionError as err:
            if "Not found" in str(err):
                pass
            else:
                raise AssertionError(f"Unexpected error message: {err}")

    def test_username_filter(self):
        self.create(
            {
                "first_name": "John",
                "last_name": "Doe",
                "username": "John_Doe",
                "email": "john@test.com",
            }
        )
        self.create(
            {
                "first_name": "Jane",
                "last_name": "Black",
                "username": "Jane_Black",
                "email": "jane@test.com",
            }
        )
        self.create(
            {
                "first_name": "Alice",
                "last_name": "Smith",
                "username": "Alice_Smith",
                "email": "alice@test.com",
            }
        )

        users_list = self.list(filters={"username": "John_Doe"})
        assert len(users_list) == 1

        users_list = self.list(filters={"first_name": "John_Doe"})
        assert len(users_list) > 3

        users_list = self.list(filters={"username": "john_doe"})
        assert len(users_list) == 0
