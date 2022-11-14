from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User

# class UserSignupAPIViewTestCase(APITestCase):
#     def test_signup(self):
#         url = reverse("user_view")
#         user_data = {
#             "email":"testcase@test.com",
#             "password":"1234"
#         }
#         response = self.client.post(url, user_data)
#         self.assertEqual(response.status_code, 200)


class LoginUserTest(APITestCase):
    def setUp(self):
        self.data = {"email":"testcase@test.com", "password":"1234"}
        self.user = User.objects.create_user("testcase@test.com", "1234")

    def test_login(self):
        url = reverse("token_obtain_pair")
        response = self.client.post(url, self.data)
        self.assertEqual(response.status_code, 200)

    def test_get_user_data(self):
        access_token = self.client.post(reverse("token_obtain_pair"), self.data).data["access"]
        response = self.client.get(
            path=reverse('user_profile_view'),
            HTTP_AUTHORIZATION=f"Bearer {access_token}"
        )
        print(response.data) # error : Reverse for 'user_profile_view' with no arguments not found / 일단 스킵