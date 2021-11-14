import time
import requests


# creating a task
task_url = "https://playground.learnqa.ru/ajax/api/longtime_job"
task_creating = requests.get(task_url)
token = task_creating.json()["token"]
seconds = task_creating.json()["seconds"]

# one request with a token before the task is ready
response_before = requests.get(task_url, params={'token': token}).json()
if response_before["status"] == "Job is NOT ready":
    print("The response to the request before the end of the processing time is correct")
    print(f"'status' = Job is NOT ready")
else:
    print("The response to the request before the end of the processing time is incorrect")

# waiting for the response result
time.sleep(seconds)

# request after the task is ready
response_after = requests.get(task_url, params={'token': token}).json()
if response_after["status"] == "Job is ready" and "result" in response_after:
    final_result = response_after["result"]
    print("The response to the request before the end of the processing time is correct")
    print(f"'status' = Job is ready")
    print(f"'result' = {final_result}")
else:
    print("The response to the request after the end of the processing time is incorrect")
