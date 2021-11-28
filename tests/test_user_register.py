from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import pytest
import random
import string


class TestUserRegister(BaseCase):
    excluded_params = [
        ("email"),
        ("password"),
        ("firstName"),
        ("lastName"),
        ("username")
    ]

    def test_create_new_user_successfully(self):
        my_data = self.prepare_registration_data()
        response = MyRequests.post("/user/", data=my_data)
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
        my_email = 'vinkotov@example.com'
        my_data = self.prepare_registration_data(my_email)
        response = MyRequests.post("/user", data=my_data)

        Assertions.assert_code_status(response, 400)
        Assertions.assert_expected_response_content(response, f"Users with email '{my_email}' already exists")

    def test_create_user_with_incorrect_email(self):
        incorrect_email = 'vinkotovexample.com'
        my_data = self.prepare_registration_data(incorrect_email)
        response = MyRequests.post("/user/", data=my_data)
        Assertions.assert_code_status(response, 400)
        Assertions.assert_expected_response_content(response, "Invalid email format")

    @pytest.mark.parametrize('missed_field', excluded_params)
    def test_create_user_without_one_params(self, missed_field):
        my_data = self.prepare_registration_data()
        del my_data[f"{missed_field}"]
        response = MyRequests.post("/user", data=my_data)

        Assertions.assert_code_status(response, 400)
        Assertions.assert_expected_response_content(response,
                                                    f"The following required params are missed: {missed_field}")

    def test_create_user_with_too_short_name(self):
        my_data = self.prepare_registration_data()
        my_data["username"] = "a"
        response = MyRequests.post("/user", data=my_data)
        Assertions.assert_code_status(response, 400)
        Assertions.assert_expected_response_content(response, "The value of 'username' field is too short")

    def test_create_user_with_too_long_name(self):
        letter = string.ascii_lowercase
        name_length = 251
        random_string = ''.join(random.choice(letter) for _ in range(name_length))
        my_data = self.prepare_registration_data()
        my_data["username"] = random_string
        response = MyRequests.post("/user", data=my_data)
        Assertions.assert_code_status(response, 400)
        Assertions.assert_expected_response_content(response, "The value of 'username' field is too long")
