from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.core.cache import cache
from django.db import DatabaseError
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
import secrets
import random
import string

from utils import sms
from .. import exceptions
from .. import messages
from .serializers import (
    UserRegistrationSerializer,
    UserPhoneActivateSerializer,
)

User = get_user_model()

class UserRegistrationView(APIView):
    @swagger_auto_schema(
        request_body=UserRegistrationSerializer(),
    )
    def post(self, request):
        """
        User registration using email, first name and last name and password
        """
        register_serializer = UserRegistrationSerializer(data=request.data)
        if register_serializer.is_valid(raise_exception=True):
            valid_data = register_serializer.validated_data
            try:
                User.objects.create_user(is_active=False, **valid_data)

            except DatabaseError:
                raise exceptions.UserNotCreated

            email = valid_data.get('email')
            token = secrets.token_urlsafe(32)
            activation_link = request.build_absolute_uri(reverse('user_activate', args=(token,)))

            # TODO: Send email by Rabbitmq and celery
            send_mail(
                subject='validation',
                message=activation_link,
                from_email= 'shortlink@gmail.com',
                recipient_list=[email]
            )

            # Save token in cache for 24 hours
            cache.set(token, email, timeout=86400)

            return Response(
                data={
                    'message': messages.USER_REGISTERED,
                },
                status=status.HTTP_201_CREATED
            )


class UserActivateView(APIView):
    def get(self, request, token):
        """
        Activation of the user account using the token stored in the cache.
        """
        email = cache.get(token)
        if not email:
            # TODO: redirect user to error page
            raise exceptions.TokenExpired
        
        user = User.objects.filter(email=email)
        user.update(is_active=True)

        # TODO: redirect user to login page
        return Response(
            data={
                'message': messages.USER_ACTIVATED,
            },
            status=status.HTTP_200_OK,
        )


class UserPhoneActivateView(APIView):
    @swagger_auto_schema(
        request_body=UserPhoneActivateSerializer(),
    )
    def post(self, request):
        """
        The mobile number is taken from the user and a confirmation code is sent to him.
        """
        CODE_LENGTH = 6
        phone_serializer = UserPhoneActivateSerializer(data=request.data)
        if phone_serializer.is_valid(raise_exception=True):
            code = ''.join(random.choice(string.digits) for i in range(CODE_LENGTH))
            phone = phone_serializer.validated_data.get('phone')
            # TODO: send SMS by Rabbitmq and celery
            sent = sms.send_validation_code(receptor=phone, token=code)
            if not sent:
                raise exceptions.SMS_NOT_SENT

            # Save code in cache for 20 minutes
            cache.set(code, phone, timeout=1200)
            return Response(
                data={
                    'message': messages.SMS_SENT,
                },
                status=status.HTTP_200_OK,
            )
