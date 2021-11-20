import requests


test_url = "https://playground.learnqa.ru/api/homework_cookie"

# expected cookie {'HomeWork': 'hw_value'}
class TestCookie:
    def test_cookie(self):
        actual_response = requests.get(test_url)
        actual_cookie = dict(actual_response.cookies)
        print(actual_cookie)
        assert "HomeWork" in actual_cookie, f"Expected cookie key 'HomeWork' is missing in the response"
        assert actual_cookie["HomeWork"] == "hw_value", f"Expected cookie value is 'hw_value'," \
                                                        f" actual cookie value is {actual_cookie['HomeWork']}"
