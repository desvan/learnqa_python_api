from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure


@allure.epic("Getting user details cases")
class TestUserGet(BaseCase):
    @allure.description("This test checks unsuccessful user details getting w/o sending auth. token and cookies")
    def test_get_user_details_not_auth(self):
        with allure.step("Try to get data of user with id=2"):
            response = MyRequests.get("/user/2")
        Assertions.assert_json_has_key(response, "username")
        unexpected_keys = ["email", "firstName", "lastName"]
        Assertions.assert_json_has_not_keys(response, unexpected_keys)

    @allure.description("This test checks getting user details: username, email, firstName, lastName, "
                        "being authorized as SAME user")
    def test_get_user_details_auth_as_same_user(self):
        my_data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        with allure.step(f"Authorize as user with id =2 and data ={my_data}"):
            response1 = MyRequests.post("/user/login", data = my_data)
            auth_sid = self.get_cookie(response1, "auth_sid")
            token = self.get_header(response1, "x-csrf-token")
            user_id_from_auth_method = self.get_json_value(response1, "user_id")

        with allure.step("Get authorized user's data"):
            response2 = MyRequests.get(
                f"/user/{user_id_from_auth_method}",
                headers = {"x-csrf-token": token},
                cookies = {"auth_sid": auth_sid}
                                     )
        expected_fields = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(response2, expected_fields)

    @allure.description("This test checks unsuccessful getting user details: username, email, firstName, lastName, "
                        "being authorized as ANOTHER user")
    def test_get_user_details_auth_as_another_user(self):
        my_data = self.prepare_registration_data()
        with allure.step("Register new generated user #1"):
            MyRequests.post("/user/", data=my_data)
        my_login_data = {
            'email': my_data['email'],
            'password': my_data['password']
            }
        with allure.step("Authorize as user #1"):
            response1 = MyRequests.post("/user/login", data = my_login_data)
            auth_sid = self.get_cookie(response1, "auth_sid")
            token = self.get_header(response1, "x-csrf-token")

        with allure.step("Try to get data of user with id=2, auth. as user #1"):
            response2 = MyRequests.get(
                "/user/2",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid}
            )

        Assertions.assert_json_has_key(response2, "username")
        unexpected_keys = ["email", "firstName", "lastName"]
        Assertions.assert_json_has_not_keys(response2, unexpected_keys)
