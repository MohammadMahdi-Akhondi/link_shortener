from rest_framework_simplejwt.authentication import JWTAuthentication
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db import DatabaseError
from django.urls import reverse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from decouple import config
from uuid import uuid4
import secrets
import random
import string

from payment.models import Transaction
from payment.idpay import IDPayAPI
from .. import exceptions
from .. import messages
from account.tasks import (
    send_html_email_task,
    send_sms_validation_code_task,
)
from .serializers import (
    UserRegistrationSerializer,
    UserPhoneActivateSerializer,
    UserPhoneVerifySerializer,
)

User = get_user_model()

class UserRegistrationView(APIView):
    serializer_class = UserRegistrationSerializer

    @swagger_auto_schema(
        request_body=serializer_class(),
    )
    def post(self, request):
        """
        User registration using email, first name and last name and password
        """
        register_serializer = self.serializer_class(data=request.data)
        if register_serializer.is_valid(raise_exception=True):
            valid_data = register_serializer.validated_data
            try:
                User.objects.create_user(**valid_data)

            except DatabaseError:
                raise exceptions.UserNotCreated

            email = valid_data.get('email')
            token = secrets.token_urlsafe(32)
            activation_link = request.build_absolute_uri(reverse('account:user_activate', args=(token,)))

            html_email = render_to_string(
                template_name='account/verify_email.html',
                context={'activation_link': activation_link},
            )
            send_html_email_task.delay(
                subject='Activate account',
                html_email=html_email,
                recipient=email,
            )

            # Save token in cache for 5 minutes
            cache.set(token, email, timeout=300)

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

        cache.delete(token)
        user = User.objects.filter(email=email)
        user.update(is_confirmed=True)

        # TODO: redirect user to login page
        return Response(
            data={
                'message': messages.USER_ACTIVATED,
            },
            status=status.HTTP_200_OK,
        )


class UserPhoneActivateView(APIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = UserPhoneActivateSerializer

    @swagger_auto_schema(
        request_body=serializer_class(),
    )
    def post(self, request):
        """
        The mobile number is taken from the user and a confirmation code is sent to him.
        """
        CODE_LENGTH = 6
        phone_serializer = self.serializer_class(data=request.data)
        if phone_serializer.is_valid(raise_exception=True):
            code = ''.join(random.choice(string.digits) for i in range(CODE_LENGTH))
            phone = phone_serializer.validated_data.get('phone')
            send_sms_validation_code_task.delay(
                receptor=phone,
                token=code,
            )

            # Save code in cache for 20 minutes
            cache.set(code, phone, timeout=1200)
            return Response(
                data={
                    'message': messages.SMS_SENT,
                },
                status=status.HTTP_200_OK,
            )


class UserPhoneVerifyView(APIView):
    authentication_classes = (JWTAuthentication, )
    permission_classes = (IsAuthenticated, )
    serializer_class = UserPhoneVerifySerializer

    @swagger_auto_schema(
        request_body=serializer_class(),
    )
    def post(self, request):
        """
        The verification code is sent and if the code is correct, it is stored in the database.
        """
        srz_verify = self.serializer_class(data=request.data)
        if srz_verify.is_valid(raise_exception=True):
            code = srz_verify.validated_data.get('code')
            phone = cache.get(code)
            if not phone:
                raise exceptions.CodeIsInvalid

            cache.delete(code)
            user = request.user
            user.phone = phone
            user.save()
            return Response(
                data={
                    'message': messages.PHONE_VERIFIED,
                },
                status=status.HTTP_200_OK,
            )


class UserUpgradeView(APIView):
    authentication_classes = (JWTAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        if request.user.phone == None:
            raise exceptions.PhoneNotRegistered

        callback = request.build_absolute_uri(reverse('payment:callback_transaction'))
        order_id = uuid4().hex[:30]
        amount = config('UPGRADE_PRICE')
        api = IDPayAPI(
            apikey=config('IDPAY_API_KEY', default='6a7f99eb-7c20-4412-a972-6dfb7cd253a4'),
            sandbox=config('IDPAY_SANDBOX'),
        )
        data = {
            'order_id': order_id,
            'amount': amount,
            'name': request.user.get_full_name(),
            'phone': request.user.phone,
            'mail': request.user.email,
            'callback': callback,
        }
        response = api.create_transaction(data=data)
        try:
            Transaction.objects.create(
                user=request.user,
                order_id=order_id,
                amount=amount,
                transaction_id=response.get('id'),
            )
        
        except DatabaseError:
            raise exceptions.SomethingWentWrong

        return Response(
            data={'link': response.get('link')},
            status=status.HTTP_200_OK,
        )
