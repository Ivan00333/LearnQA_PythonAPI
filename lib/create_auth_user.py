from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions

class CreateAuthUser:
    @staticmethod
    def user_create(register_data):
        response = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

        return response

    @staticmethod
    def user_login(email, password):
        login_data = {
            "email": email,
            "password": password
        }

        response = MyRequests.post("/user/login", data=login_data)

        Assertions.assert_code_status(response, 200)

        return response

    @staticmethod
    def create_and_login_user(register_data, email=None):
        response_user_create = CreateAuthUser.user_create(register_data)

        login_email = register_data["email"]
        password = register_data["password"]

        response_user_login = CreateAuthUser.user_login(login_email, password)

        return response_user_login

