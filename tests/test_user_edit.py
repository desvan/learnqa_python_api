from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserEdit(BaseCase):
    def test_edit_just_created_user(self):
        # REGISTER
        registration_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=registration_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = registration_data['email']
        first_name = registration_data['firstName']
        password = registration_data['password']
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_name = "changed name"

        response3 = MyRequests.put(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid},
                                   data={"firstName": new_name}
                                   )
        Assertions.assert_code_status(response3, 200)

        # GET
        response4 = MyRequests.get(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid}
                                   )
        Assertions.assert_json_value_by_name(response4,
                                             "firstName",
                                             new_name,
                                             f"Wrong name of the user after edit"
                                             )

    def test_edit_not_auth_user(self):
        response1 = MyRequests.put("/user/2",
                                   data={"firstName": "Changed_Name"}
                                   )

        Assertions.assert_code_status(response1, 400)
        Assertions.assert_expected_response_content(response1, "Auth token not supplied")

    def test_edit_user_auth_as_another_user(self):
        # REGISTER user1
        registration_data1 = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=registration_data1)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email1 = registration_data1['email']
        password1 = registration_data1['password']
        user_id1 = self.get_json_value(response1, "id")

        # REGISTER user2
        registration_data2 = self.prepare_registration_data()
        response2 = MyRequests.post("/user/", data=registration_data2)

        Assertions.assert_code_status(response2, 200)
        Assertions.assert_json_has_key(response2, "id")

        email2 = registration_data2['email']
        password2 = registration_data2['password']
        first_name2 = registration_data2['firstName']
        user_id2 = self.get_json_value(response2, "id")

        # LOGIN as user1
        login_data = {
            'email': email1,
            'password': password1
        }
        response3 = MyRequests.post("/user/login", data=login_data)
        auth_sid1 = self.get_cookie(response3, "auth_sid")
        token1 = self.get_header(response3, "x-csrf-token")

        # EDIT
        new_name = "changed name"

        response4 = MyRequests.put(f"/user/{user_id2}",
                                   headers={"x-csrf-token": token1},
                                   cookies={"auth_sid": auth_sid1},
                                   data={"firstName": new_name}
                                   )
        # print(response4.status_code)
        Assertions.assert_code_status(response4, 200)

        # LOGIN as user2
        login_data = {
            'email': email2,
            'password': password2
        }
        response5 = MyRequests.post("/user/login", data=login_data)
        auth_sid2 = self.get_cookie(response5, "auth_sid")
        token2 = self.get_header(response5, "x-csrf-token")

        # GET user2 data
        response6 = MyRequests.get(f"/user/{user_id2}",
                                   headers={"x-csrf-token": token2},
                                   cookies={"auth_sid": auth_sid2}
                                   )
        print(response6.status_code)
        print(response6.content)
        Assertions.assert_json_value_by_name(response6,
                                             "firstName",
                                             first_name2,
                                             f"Name of the user was edited by another user!"
                                             )

    def test_edit_user_email_with_incorrect_address(self):
        # REGISTER
        registration_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=registration_data)

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
        response2 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_email = "incorrect_email.com"

        response3 = MyRequests.put(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid},
                                   data={"email": new_email}
                                   )
        Assertions.assert_code_status(response3, 400)
        Assertions.assert_expected_response_content(response3, "Invalid email format")

    def test_edit_user_first_name_with_too_short_example(self):
        # REGISTER
        registration_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=registration_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = registration_data['email']
        first_name = registration_data['firstName']
        password = registration_data['password']
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_name = "a"

        response3 = MyRequests.put(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid},
                                   data={"firstName": new_name}
                                   )
        Assertions.assert_code_status(response3, 400)
        Assertions.assert_json_has_key(response3, "error")
        Assertions.assert_json_value_by_name(response3,
                                             "error",
                                             "Too short value for field firstName",
                                             "Unexpected error message!"
                                             )
