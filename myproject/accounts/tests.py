from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status


class RegisterTest(APITestCase):

    def test_register_user(self):
        data={
            'username':'surya',
            'email':'surya@gmail.com',
            'password':'surya12345'
        }

        response=self.client.post('/accounts/register/',data)

        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='surya').exists())

    def test_password_is_hashed(self):
        data={
            'username':'surya',
            'email':'surya@gmail.com',
            'password':'surya12345'
        }

        self.client.post('/accounts/register/',data)

        user=User.objects.get(username='surya')

        self.assertNotEqual(user.password,'surya12345')
        self.assertTrue(user.check_password('surya12345'))

    def test_register_without_username(self):
        data={
            'email':'surya@gmail.com',
            'password':'surya12345'
        }

        response=self.client.post('/accounts/register/',data)

        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)


class LoginTest(APITestCase):

    def setUp(self):
        self.user=User.objects.create_user(
            username='surya',
            email='surya@gmail.com',
            password='surya12345'
        )

    def test_login_user(self):
        data={
            'username':'surya',
            'password':'surya12345'
        }

        response=self.client.post('/accounts/login/',data)

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertIn('access',response.data)
        self.assertIn('refresh',response.data)

    def test_login_with_wrong_password(self):
        data={
            'username':'surya',
            'password':'wrongpassword'
        }

        response=self.client.post('/accounts/login/',data)

        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

    def test_refresh_token(self):
        login_response=self.client.post('/accounts/login/',{
            'username':'surya',
            'password':'surya12345'
        })

        refresh_token=login_response.data['refresh']

        response=self.client.post('/accounts/refresh/',{
            'refresh':refresh_token
        })

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertIn('access',response.data)
