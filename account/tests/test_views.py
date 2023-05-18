from rest_framework_simplejwt.tokens import AccessToken
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


class UserPhoneActivateTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('phone_activate')
        self.data = {'phone': '09121234567'}
        self.user = User.objects.create_user(
            email='test@gmail.com',
            password='1234',
        )
        self.access_token = AccessToken.for_user(self.user)

    def test_with_valid_phone(self):
        self.client.force_authenticate(user=self.user, token=self.access_token)
        response = self.client.post(self.url, self.data)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_unauthorized_user(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_with_invalid_data(self):
        self.client.force_authenticate(user=self.user, token=self.access_token)
        invalid_data = {'phone': '13254956527'}
        response = self.client.post(self.url, invalid_data)
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )


class UserPhoneVerifyTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('phone_verify')
        self.data = {'code': '123456'}
        self.user = User.objects.create_user(
            email='test@gmail.com',
            password='1234',
        )
        self.access_token = AccessToken.for_user(self.user)

    def test_unauthorized_user(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_with_invalid_data(self):
        self.client.force_authenticate(user=self.user, token=self.access_token)
        response = self.client.post(self.url, self.data)
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_with_valid_data(self):
        self.client.force_authenticate(user=self.user, token=self.access_token)
        phone = '09121234567'
        cache.set(self.data['code'], phone)
        response = self.client.post(self.url, self.data)
        self.user.refresh_from_db()
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            self.user.phone,
            phone,
        )
