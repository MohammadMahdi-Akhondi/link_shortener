from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

User = get_user_model()

class CreateLinkTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('create_link')
        self.data = {
            'title': 'test link',
            'real_link': 'http://test.com/'
        }
        self.user = User.objects.create_user(
            email='test@gmail.com',
            password='1234',
        )
        self.access_token = AccessToken.for_user(self.user)

    def test_with_unauthorized_user(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_with_invalid_data(self):
        invalid_data = {
            'title': 'test link',
            'real_link': 'new link'
        }
        self.client.force_authenticate(self.user, self.access_token)
        response = self.client.post(self.url, invalid_data)
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
    
    def test_with_valid_data(self):
        self.client.force_authenticate(self.user, self.access_token)
        response = self.client.post(self.url, self.data)
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )


class ListLinkView(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('list_link')
        self.user = User.objects.create_user(
            email='test@gmail.com',
            password='1234',
        )
        self.access_token = AccessToken.for_user(self.user)
    
    def test_with_unauthorized_user(self):
        response = self.client.get(self.url)
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )
    
    def test_with_valid_method(self):
        self.client.force_authenticate(self.user, self.access_token)
        response = self.client.get(self.url)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
