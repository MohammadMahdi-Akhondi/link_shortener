from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

User = get_user_model()


class UserRegistrationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('user_registration')
        self.data = {
            'first_name': 'mahdi',
            'last_name': 'Akhondi',
            'email': 'test@gmail.com',
            'password': '1234',
        }

    def test_registration_with_valid_data(self):
        response = self.client.post(self.url, self.data)
        User.objects.get(email=self.data['email'])
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        # test registration duplicate data
        response = self.client.post(self.url, self.data)
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_registration_with_invalid_method(self):
        response = self.client.get(self.url, self.data)
        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
        )


class UserActivateTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.data = {
            'first_name': 'mahdi',
            'last_name': 'Akhondi',
            'email': 'test@gmail.com',
            'password': '1234',
            'is_active': False,
        }

    def test_activate_with_valid_token(self):
        user = User.objects.create_user(**self.data)
        token = 'gjfhgewtj4-grjgr54332e_'
        cache.set(token, self.data['email'])
        url = reverse('user_activate', args=(token,))
        response = self.client.get(url)
        user.refresh_from_db()
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            user.is_active,
            True,
        )

    def test_activate_with_invalid_token(self):
        url = reverse('user_activate', args=('mahdi',))
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
