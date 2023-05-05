from rest_framework import serializers
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = (
            'first_name',
            'last_name',
            'email',
            'password',
        )
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }
