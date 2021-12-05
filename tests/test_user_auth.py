import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import allure


@allure.epic("Authorization cases")
class TestUserAuth(BaseCase):
    exclude_params = [
        ("no_cookie"),
        ("no_token")
    ]

    def setup(self):
        #   my_url = "https://playground.learnqa.ru/api/user/login"
        my_data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response1 = MyRequests.post("/user/login", data=my_data)

        self.auth_sid = self.get_cookie(response1, "auth_sid")
        self.token = self.get_header(response1, "x-csrf-token")
        self.user_id_from_auth_method = self.get_json_value(response1, "user_id")

    @allure.description("Testing successful user authorization with email and pasword")
    def test_auth_user(self):
        with allure.step("Authorize as existing user"):
            response2 = MyRequests.get("/user/auth",
                                     headers={"x-csrf-token": self.token},
                                     cookies={"auth_sid": self.auth_sid}
                                        )

        Assertions.assert_json_value_by_name(
            response2,
            "user_id",
            self.user_id_from_auth_method,
            "User id from auth method is not equal to user id from check method"
        )

    @allure.description("Testing user authorization status without sending auth. cookies or token")
    @pytest.mark.parametrize('condition', exclude_params)
    def test_negative_auth_check(self, condition):
        if condition == "no_cookie":
            with allure.step("Try to  authorize user with no cookies"):
                response3 = MyRequests.get("/user/auth",
                                         headers={"x-csrf-token": self.token}
                                         )
        else:
            with allure.step("Try to  authorize user with no token"):
                response3 = MyRequests.get("/user/auth",
                                         cookies={"auth_sid": self.auth_sid}
                                         )

        Assertions.assert_json_value_by_name(
            response3,
            "user_id",
            0,
            f"User authorized with condition '{condition}'"
        )
