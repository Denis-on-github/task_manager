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
        print(f"=== User for testing created: {self.test_user} ===")

    @staticmethod
    def expected_details(entity: dict, attributes: dict):
        return {**attributes, "id": entity["id"]}

    def test_create(self):
        print(
            "-------------------------------------------------------------------------------------------------------"
        )
        print("TEST_CREATE")
        expected_response = self.expected_details(self.test_user, self.user_attributes)
        print(f"=== Expected response: {expected_response} ===")
        assert self.test_user == expected_response
        print(
            "-------------------------------------------------------------------------------------------------------"
        )

    def test_list(self):
        print(
            "-------------------------------------------------------------------------------------------------------"
        )
        print("TEST_LIST")
        expected_response = self.expected_details(self.test_user, self.user_attributes)
        print(f"=== Expected response: {expected_response} ===")
        user_list = self.list()
        print(f"=== User list: {user_list} ===")
        assert expected_response in user_list
        print(
            "-------------------------------------------------------------------------------------------------------"
        )

    def test_retrieve(self):
        print(
            "-------------------------------------------------------------------------------------------------------"
        )
        print("TEST_RETRIEVE")
        retrieved_user = self.retrieve(self.test_user["id"])
        print(f"=== Retrieved user: {retrieved_user} ===")
        expected_response = self.expected_details(self.test_user, self.user_attributes)
        print(f"=== Expected response: {expected_response} ===")
        assert retrieved_user == expected_response
        print(
            "-------------------------------------------------------------------------------------------------------"
        )

    def test_update(self):
        print(
            "-------------------------------------------------------------------------------------------------------"
        )
        print("TEST_UPDATE")
        updated_attributes = {
            "first_name": "updated_user",
            "last_name": "updated_test",
            "username": "updated_user",
            "email": "updated_test_user@test-email.com",
            "role": User.Roles.MANAGER.value,
        }
        updated_user = self.update(self.test_user["id"], updated_attributes)
        print(f"=== Updated user: {updated_user} ===")
        expected_response = self.expected_details(updated_user, updated_attributes)
        print(f"=== Expected response: {expected_response} ===")
        assert updated_user == expected_response
        print(
            "-------------------------------------------------------------------------------------------------------"
        )

    def test_delete(self):
        print(
            "-------------------------------------------------------------------------------------------------------"
        )
        print("TEST_DELETE")
        self.delete(self.test_user["id"])
        try:
            self.retrieve(self.test_user["id"])
        except AssertionError as err:
            if "Not found" in str(err):
                pass
            else:
                raise AssertionError(f"Unexpected error message: {err}")
        print(
            "-------------------------------------------------------------------------------------------------------"
        )

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
