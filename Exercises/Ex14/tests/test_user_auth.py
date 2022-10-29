import pytest
import requests
from Exercises.Ex14.lib.base_case import BaseCase
from Exercises.Ex14.lib.assertions import Assertions

class TestUserAuth(BaseCase):
    exclude_params = [
        ('no_cookie'),
        ('no_token'),
        ("")
    ]

    def setup(self):
        data = {
            "email": "vinkotov@example.com",
            'password': '1234'
        }

        response_login = requests.post("https://playground.learnqa.ru/api/user/login", data=data)

        self.auth_cookie = self.get_cookie(response_login, "auth_sid")
        self.auth_token = self.get_header(response_login, "x-csrf-token")
        self.user_id_from_auth = self.get_json_value(response_login, "user_id")

    def test_auth_user(self):

        response_auth = requests.get(
            "https://playground.learnqa.ru/api/user/auth",
            cookies={"auth_sid": self.auth_cookie},
            headers={"x-csrf-token": self.auth_token},
        )

        Assertions.assert_json_value_by_name(
            response_auth,
            "user_id",
            self.user_id_from_auth,
            f"User id from auth method not equal from user id from check method"
        )


    @pytest.mark.parametrize('condition', exclude_params)
    def test_negative_auth_check(self, condition):

        if condition == 'no_cookie':
            response_check = requests.get(
                "https://playground.learnqa.ru/api/user/auth",
                headers={"x-csrf-token": self.auth_token}
            )
        else:
            response_check = requests.get(
                "https://playground.learnqa.ru/api/user/auth",
                cookies={"x-csrf-token": self.auth_token}
            )

        Assertions.assert_json_value_by_name(
            response_check,
            "user_id",
            0,
            f"User authorized with {condition}"
        )



