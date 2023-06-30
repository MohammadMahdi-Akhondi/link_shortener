from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from ..models import Link


User = get_user_model()

class CreateLinkTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('link:create_link')
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


class ListLinkTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('link:list_link')
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


class DetailLinkTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.owner = User.objects.create_user(
            email='test@gmail.com',
            password='1234',
        )
        self.owner_access_token = AccessToken.for_user(self.owner)
        self.link = Link.objects.create(
            title='test', real_link='http://test.com',
            token='token', user=self.owner,
        )
        self.url = reverse('link:detail_link', args=[self.link.id])

    def test_with_unauthorized_user(self):
        response = self.client.get(self.url)
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )
    
    def test_with_invalid_method(self):
        self.client.force_authenticate(self.owner, self.owner_access_token)
        response = self.client.post(self.url)
        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def test_with_another_user(self):
        user = User.objects.create_user(
            email='new@gmail.com',
            password='1234',
        )
        access_token = AccessToken.for_user(user)
        self.client.force_authenticate(user, access_token)
        response = self.client.get(self.url)
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )
    
    def test_with_valid_data(self):
        self.client.force_authenticate(self.owner, self.owner_access_token)
        response = self.client.get(self.url)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )


class UpdateLinkTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.owner = User.objects.create_user(
            email='test@gmail.com',
            password='1234',
        )
        self.owner_access_token = AccessToken.for_user(self.owner)
        self.link = Link.objects.create(
            title='test', real_link='http://test.com',
            token='token', user=self.owner,
        )
        self.url = reverse('link:update_link', args=[self.link.id])
        self.data = {
            'title': 'test',
            'real_link': 'http://new.com',
            'token': 'token',
        }
    
    def test_with_unauthorized_user(self):
        response = self.client.put(self.url)
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_with_invalid_method(self):
        self.client.force_authenticate(self.owner, self.owner_access_token)
        response = self.client.post(self.url, self.data)
        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
        )
    
    def test_with_another_user(self):
        user = User.objects.create_user(
            email='new@gmail.com',
            password='1234',
        )
        access_token = AccessToken.for_user(user)
        self.client.force_authenticate(user, access_token)
        response = self.client.put(self.url, self.data)
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )
    
    def test_with_invalid_data(self):
        invalid_data = {
            'real_link': 'new',
            'token': 'token',
        }
        self.client.force_authenticate(self.owner, self.owner_access_token)
        response = self.client.put(self.url, invalid_data)
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
    
    def test_with_valid_data(self):
        self.client.force_authenticate(self.owner, self.owner_access_token)
        response = self.client.put(self.url, self.data)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )


class DeleteLinkTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.owner = User.objects.create_user(
            email='test@gmail.com',
            password='1234',
        )
        self.owner_access_token = AccessToken.for_user(self.owner)
        self.link = Link.objects.create(
            title='test', real_link='http://test.com',
            token='token', user=self.owner,
        )
        self.url = reverse('link:delete_link', args=[self.link.id])

    def test_with_unauthorized_user(self):
        response = self.client.delete(self.url)
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )
    
    def test_with_invalid_method(self):
        self.client.force_authenticate(self.owner, self.owner_access_token)
        response = self.client.post(self.url)
        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def test_with_another_user(self):
        user = User.objects.create_user(
            email='new@gmail.com',
            password='1234',
        )
        access_token = AccessToken.for_user(user)
        self.client.force_authenticate(user, access_token)
        response = self.client.delete(self.url)
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_with_valid_data(self):
        self.client.force_authenticate(self.owner, self.owner_access_token)
        response = self.client.delete(self.url)
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )


class RedirectLinkTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.owner = User.objects.create_user(
            email='test@gmail.com',
            password='1234',
        )
        self.link = Link.objects.create(
            title='test', real_link='http://test.com',
            token='token', user=self.owner,
        )
        self.url = reverse('link:redirect_link', args=[self.link.token])

    def test_with_invalid_method(self):
        response = self.client.post(self.url)
        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def test_with_guest_user(self):
        response = self.client.get(self.url)
        self.assertEqual(
            response.status_code,
            status.HTTP_302_FOUND,
        )
