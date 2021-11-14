import requests


my_url = "https://playground.learnqa.ru/ajax/api/compare_query_type"

response1 = requests.get(my_url)
print(f"1. HTTP request without params: {response1.text}", end="\n\n")

response2 = requests.head(my_url, params={"method": "HEAD"})
print(f"2. HTTP request with method HEAD: {response2.text}", end="\n\n")

response3 = requests.get(my_url, params={"method": "GET"})
print(f"3. Request with the correct method (method GET): {response3.text}", end="\n\n")

print("4. Possible bugs:")
methods = ["GET", "POST", "PUT", "DELETE"]
for request_method in methods:
    for params_method in methods:
        if request_method == "GET":
            response = requests.request(method=request_method, url=my_url, params={"method": params_method})
        else:
            response = requests.request(method=request_method, url=my_url, data={"method": params_method})

        if request_method == params_method and response.text != response3.text:
            print(f"Bug found. HTTP request with method {request_method} and params/data method {params_method}")
            print(f"Expected result: {response3.text}")
            print(f"Actual result: {response1.text}", end="\n\n")
        elif request_method != params_method and response.text == response3.text:
            print(f"Bug found. HTTP request with method {request_method} and params/data method {params_method}")
            print(f"Expected result: {response1.text}")
            print(f"Actual result: {response3.text}", end="\n\n")
