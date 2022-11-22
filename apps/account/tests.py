# from audioop import reverse
# import json

# from django.contrib.auth import get_user_model
# # from django.urls import reverse
# from rest_framework import status

# from rest_framework.test import APITestCase

# from .models import User
# # from .serializers import RegistrationSerializer

# User = get_user_model()

# class RegistrationTestCase(APITestCase):
#     def test_register(self):
#         data = {"username": "test", "phone": "+996703491179", "password": "1", "password_confirm": "1"}
#         url = reverse("/api/account/registration/")

#         # response = self.client.post("/api/account/registration/", data)
#         # self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(User.objects.count(), 1)
#         self.assertEqual(User.objects.get().username, 'test')