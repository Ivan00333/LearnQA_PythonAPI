import requests

url = "https://playground.learnqa.ru/ajax/api/compare_query_type"


"""Делаем http-запрос любого типа без параметра method"""

response = requests.get(url)
print(f"Текст ответа на GET запрос без параметра method - {response.text}")
print(f"Статус код GET запроса без параметра method - {response.status_code}")
print()

"""Делаем HEAD запрос"""

head_response = requests.head(url)
print(f"Текст ответа на HEAD запрос без параметра method - {head_response.text}")
print(f"Статус код HEAD запроса без параметра method - {head_response.status_code}")
print()

"""Делаем запрос с правильным значением method"""

true_get_response = requests.get(url, params={"method": "GET"})
print(f"Текст ответа с правильным значением method - {true_get_response.text}")
print(f"Статус код на запрос с правильным значением method - {true_get_response.status_code}")
print()

"""Проверка всеx возможные сочетания реальных типов запроса и значений параметра method"""

print("Проверка все возможные сочетания реальных типов запроса и значений параметра method:")
methods = ["POST", "GET", "PUT", "DELETE"]
for i in methods:
    response_get_check_all_types = requests.get(url, params={"method": i})
    print(f"Текст ответа GET запроса со значением method: {i} - {response_get_check_all_types.text}")
    print(f"Статус код GET запроса со значением method: {i} - {response_get_check_all_types.status_code}")
print()

requests_types = [requests.post, requests.put, requests.delete]

methods_not_get = ["POST", "PUT", "DELETE"]
index_requests_types = 0

for i in requests_types:
    for k in methods:
        response_check_all_types = i(url, params={"method": k})
        print(f"Текст ответа {methods_not_get[index_requests_types]} запроса со значением method: {k} - {response_check_all_types.text}")
        print(f"Статус код {methods_not_get[index_requests_types]} запроса со значением method: {k} - {response_check_all_types.status_code}")
    index_requests_types += 1
    print()