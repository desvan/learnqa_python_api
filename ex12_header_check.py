import requests

test_url = "https://playground.learnqa.ru/api/homework_header"


class TestHeader:
    def test_header(self):
        print("Expected header is {'x-secret-homework-header': 'Some secret value'}")
        actual_response = requests.get(test_url)
        actual_header = dict(actual_response.headers)
        assert actual_response.status_code == 200, 'Wrong response code'
        assert "x-secret-homework-header" in actual_header, f"Expected header key 'x-secret-homework-header' " \
                                                            f"is missing in the response"
        assert actual_header["x-secret-homework-header"] == "Some secret value", \
            f"Expected cookie value: 'Some secret value', actual header value: {actual_header['x-secret-homework-header']}"
