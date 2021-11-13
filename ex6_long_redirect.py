import requests


response = requests.get("https://playground.learnqa.ru/api/long_redirect")

redirects_amount = len(response.history)
final_response = response.url

print(f"Amount of redirects is {redirects_amount}")
print(f"Final response is {final_response}")
