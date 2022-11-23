from rest_framework import status, response
from rest_framework.test import APITestCase


class RegistrationTestCase(APITestCase):

    def test_register(self):
        data = {"username": "test", "phone": "+996703491179", "password": "1", "password_confirm": "1"}

        response = self.client.post("/api/account/registration/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)