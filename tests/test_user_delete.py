import allure

from lib.create_auth_user import CreateAuthUser
from lib.base_case import BaseCase
from lib.my_requests import MyRequests
from lib.assertions import Assertions


@allure.epic("Delete user cases")
class TestUserDelete(BaseCase):
    @allure.title("Delete user with ID=2")
    def test_delete_user_with_id2(self):
        email = 'vinkotov@example.com'
        password = '1234'

        with allure.step("Login user"):
            response_login_user = CreateAuthUser.user_login(email, password)
            token = self.get_header(response_login_user, "x-csrf-token")
            cookie = self.get_cookie(response_login_user, "auth_sid")
            user_id = self.get_json_value(response_login_user, "user_id")

        with allure.step("Delete user"):
            response_delete = MyRequests.delete(
                f"user/{user_id}",
                cookies={"auth_sid": cookie},
                headers={"x-csrf-token": token}
            )
            Assertions.assert_code_status(response_delete, 404)

        with allure.step("Get user"):
            response = MyRequests.get(f"/user/{user_id}")

            Assertions.assert_json_has_key(response, "username")
            Assertions.assert_json_has_not_key(response, "email")
            Assertions.assert_json_has_not_key(response, "firstName")
            Assertions.assert_json_has_not_key(response, "lastName")

    @allure.title("Delete user successful")
    def test_delete_user_successful(self):

        with allure.step("create and login user"):
            register_data = self.prepare_registration_data()
            response_user = CreateAuthUser.create_and_login_user(register_data)

            token = self.get_header(response_user, "x-csrf-token")
            cookie = self.get_cookie(response_user, "auth_sid")
            user_id = self.get_json_value(response_user, "user_id")

        with allure.step("Delete user"):
            response_delete = MyRequests.delete(
                f"/user/{user_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": cookie}
                )

            Assertions.assert_code_status(response_delete, 200)

        with allure.step("Get user"):
            response_get_user = MyRequests.get(f"/user/{user_id}")

            Assertions.assert_code_status(response_get_user, 404)
            assert response_get_user.text == "User not found", f"Response text is {response_delete.text}"

    @allure.title("Delete user by another user")
    def test_delete_another_user(self):

        with allure.step("Create and login user1"):
            register_data_user1 = self.prepare_registration_data()

            response_user1 = CreateAuthUser.create_and_login_user(register_data_user1)
            user1_id = self.get_json_value(response_user1, "user_id")

        with allure.step("Login user2"):
            register_data_user2 = self.prepare_registration_data()

            response_login_user2 = CreateAuthUser.create_and_login_user(register_data_user2)
            token_user2 = self.get_header(response_login_user2, "x-csrf-token")
            cookie_user2 = self.get_cookie(response_login_user2, "auth_sid")
            user2_id = self.get_json_value(response_login_user2, "user_id")


        with allure.step("Delete user1"):
            response_delete = MyRequests.delete(
                f"/user/{user1_id}",
                headers={"x-csrf-token": token_user2},
                cookies={"auth_sid": cookie_user2}
                )

            Assertions.assert_code_status(response_delete, 400)

        with allure.step("Get user1"):
            response_get_user = MyRequests.get(f"/user/{user1_id}")

            Assertions.assert_code_status(response_get_user, 200)
            Assertions.assert_json_has_key(response_get_user, "username")