import requests
import time

url = "https://playground.learnqa.ru/ajax/api/longtime_job"

create_task_response = requests.get(url).json()
token = {"token": create_task_response["token"]}
seconds = create_task_response["seconds"]

job_is_not_ready_response = requests.get(url, params=token).json()
status = "Job is ready"
key_result = "result"

if job_is_not_ready_response["status"] != 'Job is NOT ready':
    print("Неверный статус задачи!")
else:
    time.sleep(seconds)
    job_is_ready_response = requests.get(url, params=token).json()
    if job_is_ready_response["status"] == status:
        print(status)
    else:
        print("Статус не верный")
    if key_result in job_is_ready_response:
        print(f"Результат задачи - {job_is_ready_response[key_result]}")
    else:
        print("Результат не верный")