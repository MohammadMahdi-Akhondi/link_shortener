from django.contrib.auth import get_user_model
from django.db import DatabaseError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import UserRegistrationSerializer
from .. import exceptions
from .. import messages

User = get_user_model()

class UserRegistrationView(APIView):
    def post(self, request):
        register_serializer = UserRegistrationSerializer(data=request.data)
        if register_serializer.is_valid(raise_exception=True):
            valid_data = register_serializer.validated_data
            try:
                User.objects.create_user(is_active=False, **valid_data)

            except DatabaseError:
                raise exceptions.UserNotCreated

            # TODO: send validation email to user

            return Response(
                data={
                    'message': messages.USER_REGISTERED,
                },
                status=status.HTTP_201_CREATED
            )
