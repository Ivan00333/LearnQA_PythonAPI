import requests
import pytest

def test_cookie():
    response = requests.get("https://playground.learnqa.ru/api/homework_cookie")
    print(response.cookies)
    cookie_key = "HomeWork"
    cookie_value = "hw_value"
    cookies = response.cookies
    assert cookie_key in cookies, f"There is no cookie with key '{cookie_key}'"
    assert cookies.get(cookie_key) == cookie_value, f"'{cookie_key}' doesn't have value '{cookie_value}'"
