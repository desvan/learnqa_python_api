from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure
import time


@allure.epic("User deleting cases")
class TestUserDelete(BaseCase):
    @allure.description("This test checks authorized protected user can not delete himself")
    def test_delete_protected_user(self):
        user_data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        with allure.step(f"Authorize as user with id=2 and data={user_data}"):
            response1 = MyRequests.post("/user/login", data=user_data)
            auth_sid = self.get_cookie(response1, "auth_sid")
            token = self.get_header(response1, "x-csrf-token")
        with allure.step("Try to delete user with id=2"):
            response2 = MyRequests.delete(f"/user/2",
                                          headers={"x-csrf-token": token},
                                          cookies={"auth_sid": auth_sid},
                                          )
        Assertions.assert_code_status(response2, 400)
        Assertions.assert_expected_response_content(response2,
                                                    "Please, do not delete test users with ID 1, 2, 3, 4 or 5.")

    @allure.description("This test checks successful deleting authorized user")
    def test_delete_user_successfully(self):
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
        with allure.step(f"Authorize as registered user with data={login_data}"):
            response2 = MyRequests.post("/user/login", data=login_data)
            auth_sid = self.get_cookie(response2, "auth_sid")
            token = self.get_header(response2, "x-csrf-token")

        # DELETE
        with allure.step("Try to delete authorized user"):
            response3 = MyRequests.delete(f"/user/{user_id}",
                                          headers={"x-csrf-token": token},
                                          cookies={"auth_sid": auth_sid},
                                          )
        Assertions.assert_code_status(response3, 200)

        # GET
        with allure.step("Check user is deleted"):
            response4 = MyRequests.get(f"/user/{user_id}",
                                       headers={"x-csrf-token": token},
                                       cookies={"auth_sid": auth_sid}
                                       )
        Assertions.assert_code_status(response4, 404)
        Assertions.assert_expected_response_content(response4, "User not found")

    @allure.description("This test checks authorized user can not delete another user")
    def test_delete_user_auth_as_another_user(self):
        # REGISTER user1
        with allure.step("Register new generated user #1"):
            response1, registration_data1 = self.generate_new_user()

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email1 = registration_data1['email']
        password1 = registration_data1['password']
        time.sleep(2)

        # REGISTER user2
        with allure.step("Register new generated user #2"):
            response2, registration_data2 = self.generate_new_user()

        Assertions.assert_code_status(response2, 200)
        Assertions.assert_json_has_key(response2, "id")

        email2 = registration_data2['email']
        password2 = registration_data2['password']
        user2_id = self.get_json_value(response2, "id")

        # LOGIN as user1
        login_data = {
            'email': email1,
            'password': password1
        }
        with allure.step("Authorize as user #1"):
            response3 = MyRequests.post("/user/login", data=login_data)
            auth_sid1 = self.get_cookie(response3, "auth_sid")
            token1 = self.get_header(response3, "x-csrf-token")

        # DELETE user2 by user1
        with allure.step("Try to delete user #2"):
            MyRequests.delete(f"/user/{user2_id}",
                              headers={"x-csrf-token": token1},
                              cookies={"auth_sid": auth_sid1}
                              )
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
        with allure.step("Check user #2 still exists"):
            response6 = MyRequests.get(f"/user/{user2_id}",
                                       headers={"x-csrf-token": token2},
                                       cookies={"auth_sid": auth_sid2}
                                       )
        Assertions.assert_json_has_key(response6, "id")
