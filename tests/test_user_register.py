from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import pytest
import random
import string
import allure


letters = string.ascii_lowercase
rand_string = ''.join(random.choice(letters) for i in range(251))


@allure.epic("User registration cases")
class TestUserRegister(BaseCase):
    incorrect_data_set = [
        ({'email': 'vinkotovexample.com'}, ("Invalid email format")),
        ({'firstName': "c"}, ("The value of 'firstName' field is too short")),
        ({'firstName': rand_string}, ("The value of 'firstName' field is too long"))
    ]

    excluded_params = [
        ("email"),
        ("password"),
        ("firstName"),
        ("lastName"),
        ("username")
    ]

    @allure.description("This test checks successful user registration using email and password"
                        "and filling in 'firstName', 'lastName', and 'username' fields")
    def test_create_new_user_successfully(self):
        my_data = self.prepare_registration_data()
        with allure.step("Register new generated user"):
            response = MyRequests.post("/user/", data = my_data)
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
        my_email = 'vinkotov@example.com'
        my_data = self.prepare_registration_data(my_email)
        with allure.step(f"Try to register existing user with email={my_email}"):
            response = MyRequests.post("/user", data = my_data)

        Assertions.assert_code_status(response, 400)
        Assertions.assert_expected_response_content(response, f"Users with email '{my_email}' already exists")

    @allure.description("This test checks unsuccessful user registration"
                        "using email with incorrect format, too short or too long first name of user")
    @pytest.mark.parametrize("wrong_data, expected_error_message", incorrect_data_set)
    def test_create_user_with_incorrect_data(self, wrong_data, expected_error_message):
        my_data = self.prepare_registration_data()
        my_data.update(wrong_data)
        with allure.step(f"Try to register new user with incorrect data = {my_data}"):
            response=MyRequests.post("/user", data=my_data)

        Assertions.assert_code_status(response, 400)
        Assertions.assert_expected_response_content(response, expected_error_message)

    @allure.description("This test checks unsuccessful user registration"
                        " with any of required user data fields missed")
    @pytest.mark.parametrize('missed_field', excluded_params)
    def test_negative_register_check(self, missed_field):
        my_data = self.prepare_registration_data()
        del my_data[f"{missed_field}"]
        with allure.step(f"Try to register new user with data field '{missed_field}' missing"):
            response = MyRequests.post("/user", data=my_data)

        Assertions.assert_code_status(response, 400)
        Assertions.assert_expected_response_content(response, f"The following required params are missed: {missed_field}")
