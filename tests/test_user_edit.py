import allure

from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.create_auth_user import CreateAuthUser

@allure.epic("Edit user cases")
class TestUserEdit(BaseCase):

    @allure.title("Edit just crated user")
    def test_edit_just_created_user(self):
        with allure.step("Register and login user"):
            register_data = self.prepare_registration_data()
            response_user_login = CreateAuthUser.create_and_login_user(register_data)
            user_id = self.get_json_value(response_user_login, "user_id")

            auth_sid = self.get_cookie(response_user_login, "auth_sid")
            token = self.get_header(response_user_login, "x-csrf-token")

        with allure.step("Edit user"):
            new_name = 'Changed Name'

            response_user_edit = MyRequests.put(
                f"/user/{user_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid},
                data={"firstName": new_name}
            )

            Assertions.assert_code_status(response_user_edit, 200)

        with allure.step("Get user"):
            response_get_user = MyRequests.get(
                f"/user/{user_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid}
            )

            Assertions.assert_json_value_by_name(
                response_get_user,
                "firstName",
                new_name,
                "Wrong name of the user after edit"
            )

    @allure.title("Edit user by unauthorized user")
    def test_edit_not_auth_user(self):
        response = MyRequests.put(
            f"/user/2",
            data={"firstName": "New name"}
        )

        Assertions.assert_code_status(response, 400)
        assert response.text == "Auth token not supplied", f"Response text is {response.text}"

    @allure.title("Edit user by another user")
    def test_edit_another_auth_user(self):
        with allure.step("Create and login user1"):
            user1_register_data = self.prepare_registration_data()
            response_login_user1 = CreateAuthUser.create_and_login_user(user1_register_data)
            user1_id = self.get_json_value(response_login_user1, "user_id")
            user1_auth_sid = self.get_cookie(response_login_user1, "auth_sid")
            user1_token = self.get_header(response_login_user1, "x-csrf-token")

            first_name_user1 = user1_register_data["firstName"]

        with allure.step("Create and login user2"):
            user2_register_data = self.prepare_registration_data()
            response_login_user2 = CreateAuthUser.create_and_login_user(user2_register_data)
            user2_id = self.get_json_value(response_login_user1, "user_id")
            user2_auth_sid = self.get_cookie(response_login_user1, "auth_sid")
            user2_token = self.get_header(response_login_user1, "x-csrf-token")

        with allure.step("Edit user1 by user2"):
            new_name = 'Changed Name'

            response_user_edit = MyRequests.put(
                f"/user/{user1_id}",
                headers={"x-csrf-token": user2_token},
                cookies={"auth_sid": user2_auth_sid},
                data={"firstName": new_name}
            )

            Assertions.assert_code_status(response_user_edit, 400)

        with allure.step("Get user1"):
            response_get_user = MyRequests.get(
                f"/user/{user1_id}",
                headers={"x-csrf-token": user1_token},
                cookies={"auth_sid": user1_auth_sid}
            )

            Assertions.assert_json_value_by_name(
                response_get_user,
                "firstName",
                first_name_user1,
                "Wrong name of the user after edit"
            )

    @allure.title("Change user email without symbol @")
    def test_change_user_email_without_symbol(self):
        with allure.step("Create and login user1"):
            register_data = self.prepare_registration_data()
            response_user_login = CreateAuthUser.create_and_login_user(register_data)

            email = register_data["email"]

            auth_sid = self.get_cookie(response_user_login, "auth_sid")
            token = self.get_header(response_user_login, "x-csrf-token")
            user_id = self.get_json_value(response_user_login, "user_id")

        with allure.step("Edit user"):
            new_email = 'changed.ru'

            response_user_edit = MyRequests.put(
                f"/user/{user_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid},
                data={"email": new_email}
            )

            Assertions.assert_code_status(response_user_edit, 400)
            assert response_user_edit.text == "Invalid email format", f"Response text is {response_user_edit.text}"

        with allure.step("Get user"):
            response_get_user = MyRequests.get(
                f"/user/{user_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid}
            )

            Assertions.assert_json_value_by_name(
                response_get_user,
                "email",
                email,
                "Wrong email of the user after edit"
            )


    @allure.title("Change firstname short value")
    def test_change_firstname_short_value(self):

        with allure.step("create and login user1"):
            register_data = self.prepare_registration_data()
            response_user_login = CreateAuthUser.create_and_login_user(register_data)

            first_name = register_data["firstName"]

            auth_sid = self.get_cookie(response_user_login, "auth_sid")
            token = self.get_header(response_user_login, "x-csrf-token")
            user_id = self.get_json_value(response_user_login, "user_id")

        with allure.step("Edit user"):
            new_name = 'c'

            response_user_edit = MyRequests.put(
                f"/user/{user_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid},
                data={"firstName": new_name}
            )

            Assertions.assert_code_status(response_user_edit, 400)
            Assertions.assert_json_has_key(response_user_edit, "error")
            Assertions.assert_json_value_by_name(response_user_edit, "error", "Too short value for field firstName", "Wrong response text")

        with allure.step("Get user"):
            response_get_user = MyRequests.get(
                f"/user/{user_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid}
            )

            Assertions.assert_json_value_by_name(
                response_get_user,
                "firstName",
                first_name,
                "Wrong name of the user after edit"
            )


