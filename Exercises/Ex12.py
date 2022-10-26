import requests
import pytest

def test_cookie():
    response = requests.get("https://playground.learnqa.ru/api/homework_header")
    print(response.headers)
    header_key = 'x-secret-homework-header'
    header_value = 'Some secret value'
    headers = response.headers
    assert header_key in headers, f"There is no cookie with key '{header_key}'"
    assert headers.get(header_key) == header_value, f"'{header_key}' doesn't have value '{header_value}'"