import requests

response = requests.get("https://playground.learnqa.ru/api/long_redirect", allow_redirects=True)
number_of_redirects = len(response.history)
print(f"Количество редиректов - {number_of_redirects}")

first_response = response.history[0]
second_response = response
print(f"Первый url - {first_response.url}")
print(f"Второй url - {second_response.url}")