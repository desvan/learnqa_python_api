import requests


test_url = "https://playground.learnqa.ru/api/homework_cookie"

class TestCookie:
    def test_cookie(self):
        print("Expected cookie is {'HomeWork': 'hw_value'}")
        actual_response = requests.get(test_url)
        actual_cookie = dict(actual_response.cookies)
        assert actual_response.status_code == 200, 'Wrong response code'
        assert "HomeWork" in actual_cookie, f"Expected cookie key 'HomeWork' is missing in the response"
        assert actual_cookie["HomeWork"] == "hw_value", f"Expected cookie value: 'hw_value'," \
                                                        f" actual cookie value: {actual_cookie['HomeWork']}"
