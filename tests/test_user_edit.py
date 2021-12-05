from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import pytest
import allure


@allure.epic("User edition cases")
class TestUserEdit(BaseCase):
    @allure.description("This test checks authorized user can edit his registration data")
    def test_edit_just_created_user(self):
        # REGISTER
        with allure.step("Register new generated user"):
            response1, registration_data = self.generate_new_user()

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = registration_data['email']
        password = registration_data['password']
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        with allure.step("Authorize as new registered user"):
            response2 = MyRequests.post("/user/login", data=login_data)
            auth_sid = self.get_cookie(response2, "auth_sid")
            token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_name = "changed name"

        with allure.step(f"Try to change user's first name to {new_name}"):
            response3 = MyRequests.put(f"/user/{user_id}",
                                       headers={"x-csrf-token": token},
                                       cookies={"auth_sid": auth_sid},
                                       data={"firstName": new_name}
                                       )

        Assertions.assert_code_status(response3, 200)

        # GET
        with allure.step("Get authorized user's new data"):
            response4 = MyRequests.get(f"/user/{user_id}",
                                       headers={"x-csrf-token": token},
                                       cookies={"auth_sid": auth_sid}
                                       )

        Assertions.assert_json_value_by_name(response4,
                                             "firstName",
                                             new_name,
                                             f"Wrong name of the user after edit"
                                             )

    @allure.description("This test checks unsuccessful user edition without sending auth. cookies and token")
    def test_edit_not_auth_user(self):
        new_name = "Changed_Name"
        with allure.step(f"Try to edit first name of user with id=2 to {new_name}"):
            response1 = MyRequests.put("/user/2",
                                       data={"firstName": new_name}
                                       )

        Assertions.assert_code_status(response1, 400)
        Assertions.assert_expected_response_content(response1, "Auth token not supplied")

    @allure.description("This test checks unsuccessful user edition using another user auth data")
    def test_edit_user_auth_as_another_user(self):
        # REGISTER user1
        with allure.step("Register new generated user #1"):
            response1, registration_data1 = self.generate_new_user()

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email1 = registration_data1['email']
        password1 = registration_data1['password']

        # REGISTER user2
        with allure.step("Register new generated user #2"):
            response2, registration_data2 = self.generate_new_user()

        Assertions.assert_code_status(response2, 200)
        Assertions.assert_json_has_key(response2, "id")

        email2 = registration_data2['email']
        password2 = registration_data2['password']
        first_name2 = registration_data2['firstName']
        user_id2 = self.get_json_value(response2, "id")

        # LOGIN as user1
        login_data1 = {
            'email': email1,
            'password': password1
        }
        with allure.step("Authorize as user #1"):
            response3 = MyRequests.post("/user/login", data=login_data1)
            auth_sid1 = self.get_cookie(response3, "auth_sid")
            token1 = self.get_header(response3, "x-csrf-token")

        # EDIT
        new_name = "changed name"

        with allure.step(f"Try to edit first name of user #2 to '{new_name}' being auth as user #1"):
            response4 = MyRequests.put(f"/user/{user_id2}",
                                       headers={"x-csrf-token": token1},
                                       cookies={"auth_sid": auth_sid1},
                                       data={"firstName": new_name}
                                       )

        Assertions.assert_code_status(response4, 200)

        # LOGIN as user2
        login_data2 = {
            'email': email2,
            'password': password2
        }
        with allure.step("Authorize as user #2"):
            response5 = MyRequests.post("/user/login", data=login_data2)
            auth_sid2 = self.get_cookie(response5, "auth_sid")
            token2 = self.get_header(response5, "x-csrf-token")

        # GET user2 data
        with allure.step("Get user #2 data"):
            response6 = MyRequests.get(f"/user/{user_id2}",
                                       headers={"x-csrf-token": token2},
                                       cookies={"auth_sid": auth_sid2}
                                       )

        Assertions.assert_json_value_by_name(response6,
                                             "firstName",
                                             first_name2,
                                             f"Name of the user was edited by another user!"
                                             )

    incorrect_data = [
        ({'email': "incorrect_email.com"}, (400, "Invalid email format")),
        ({'firstName': "c"}, (400, "Too short value for field firstName"))
    ]

    @allure.description("This test checks unsuccessful user edition using email with incorrect format "
                        "or too short user first name")
    @pytest.mark.parametrize("input_data, expected_result", incorrect_data)
    def test_edit_user_with_incorrect_data(self, input_data, expected_result):
        # REGISTER
        with allure.step("Register new generated user"):
            response1, registration_data = self.generate_new_user()

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = registration_data['email']
        password = registration_data['password']
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        with allure.step("Authorize as new user"):
            response2 = MyRequests.post("/user/login", data=login_data)
            auth_sid = self.get_cookie(response2, "auth_sid")
            token = self.get_header(response2, "x-csrf-token")

        # EDIT
        with allure.step("Try to edit user with incorrect data"):
            response3 = MyRequests.put(f"/user/{user_id}",
                                       headers={"x-csrf-token": token},
                                       cookies={"auth_sid": auth_sid},
                                       data=input_data
                                       )
        expected_status_code, expected_text = expected_result
        Assertions.assert_code_status(response3, expected_status_code)
        assert expected_text in response3.text
