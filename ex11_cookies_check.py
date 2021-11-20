import requests


# Getting the expected cookie
# test_url = "https://playground.learnqa.ru/api/homework_cookie"
# response = requests.get(test_url)
# print(response.cookies)
# expected_cookies = dict(response.cookies)
# print(expected_cookies)

class TestPhrase:
    def test_cookies(self):
        expected_cookies = {'HomeWork': 'hw_value'}
        test_url = "https://playground.learnqa.ru/api/homework_cookie"
        test_response = requests.get(test_url)
        actual_cookies = dict(test_response.cookies)
        assert expected_cookies == actual_cookies, f"Excpected cookies is {expected_cookies}. " \
                                                   f"Actual cookies is {actual_cookies}"
