# import profile
# from django.test import TestCase
# from rest_framework import status, response
# from rest_framework.test import APITestCase
# from django.contrib.auth import get_user_model
# from rest_framework_simplejwt.tokens import RefreshToken
# from django.urls import reverse
# from rest_framework.test import APIClient


# from .models import UserProfile



# User = get_user_model()


# def get_tokens_for_user(user):
#     refresh = RefreshToken.for_user(user)

#     return {
#         'refresh': str(refresh),
#         'access': str(refresh.access_token),
#     }




# class ProfileTestCase(APITestCase):

#     def test_prifile(self):
#         # data = {"first_name": "test", "last_name": "test", "bio": "test", 
#         # "avatar": "media/Screenshot_from_2022-11-16_23-48-31_G5aOwLw.png", 
#         # "birthday": "2005-08-05", "phone": "+996703491179"
#         # }

#         self.admin1_token = get_tokens_for_user(self.admin1)


#         self.admin1 = UserProfile.objects.create(
#             first_name='test',
#             last_name='test',
#             bio='x',
#             avatar='Screenshot_from_2022-11-16_23-48-31_G5aOwLw.png',
#             birthday='2005-08-05',
#             phone='+996703491179',
#             # user=User.objects.get('user')
#             HTTP_AUTHORIZATION=f'Bearer {self.admin1_token.get("access")}'
#         )

#         data = profile.copy()
#         self.admin1_token = get_tokens_for_user(self.admin1)


#         client = APIClient()
#         client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin1_token.get("access")}')

#         response = self.client.post("/api/profile/", data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)








# class TestProfile(TestCase):
#     def setUp(self):
#         self.user1 = User.objects.create_user(
#             phone='+996703491179',
#             password='1',
#             password_ocnfirm='1',
#             username='testuser',
#             is_active=True
#         )
#         self.admin1 = User.objects.create_superuser(
#             phone='+996703491179',
#             password='1',
#             password_confirm='1',
#             username='superuser1'
#         )
#         self.user1_token = get_tokens_for_user(self.user1)
#         self.admin1_token = get_tokens_for_user(self.admin1)

#         self.profile = UserProfile.objects.create(
#             first_name='test',
#             last_name='test',
#             bio='x',
#             avatar='Screenshot_from_2022-11-16_23-48-31_G5aOwLw.png',
#             birthday='2005-08-05',
#             phone='+996703491179'
#         )

#         # def test_create_product_as_superuser(self):
#         # data = self.product_payload.copy()
#         # client = APIClient()
#         # url = 'http://localhost:8000/products/'
#         # client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin1_token.get("access")}')
#         # response = client.post(url, data)
#         # self.assertEqual(response.status_code, 201)

#         def create_profile_as_user(self):
#             data = self.profile.copy()
#             client = APIClient()
#             url = 'http://localhost:8000/profile/'
#                     client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin1_token.get("access")}')









