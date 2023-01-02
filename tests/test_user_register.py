import pytest

from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions

import allure


@allure.epic("Autorization cases")
class TestUserRegister(BaseCase):
    exclude_params = [
        ({
        "password": "",
        "username": "learnqa",
        "firstName": "learnqa",
        "lastName": "learnqa",
        "email": "test@test.ru"
        }), ({
        "password": "123",
        "username": "",
        "firstName": "learnqa",
        "lastName": "learnqa",
        "email": "test@test.ru"
        }), ({
        "password": "123",
        "username": "learnqa",
        "firstName": "",
        "lastName": "learnqa",
        "email": "test@test.ru"
        }), ({
        "password": "123",
        "username": "learnqa",
        "firstName": "learnqa",
        "lastName": "",
        "email": "test@test.ru"
        }), ({
        "password": "123",
        "username": "learnqa",
        "firstName": "learnqa",
        "lastName": "learnqa",
        "email": ""
        }),

    ]

    value = [
        ('l'),
        ('l' * 251)
    ]

    @allure.title("Create user successfuly")
    def test_create_user_successfuly(self):
        data = self.prepare_registration_data()

        response =MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    @allure.title("Create user with existing email")
    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode('utf-8') == f"Users with email '{email}' already exists", f"Unexpected response content {response.content}"

    @allure.title("Create user with not correct email")
    def test_create_user_with_not_correct_email(self):
        email = 'vinkotovexample.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode('utf-8') == f"Invalid email format"

    @allure.title("Create user without one of parameters")
    @pytest.mark.parametrize('data', exclude_params)
    def test_create_user_without_value(self, data):

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        for key, value in data.items():
            if value == "":
                break
        assert response.text == f"The value of '{key}' field is too short"

    @allure.title("Registration user with short and long userName")
    @pytest.mark.parametrize('username_value', value)
    def test_short_username(self, username_value):
        data = {
        "password": "123",
        "username": username_value,
        "firstName": "learnqa",
        "lastName": "learnqa",
        "email": "test@test.ru"
        }

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)

        if len(username_value) == 1:
            assert response.text == "The value of 'username' field is too short"
        else:
            assert response.text == "The value of 'username' field is too long"