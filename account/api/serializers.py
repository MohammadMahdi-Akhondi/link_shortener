from rest_framework import serializers
from django.contrib.auth import get_user_model


from payment.models import Transaction

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
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


class UserPhoneActivateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'phone',
        )
    
    def validate_phone(self, phone):
        pattern = r'^09\d{9}$'
        if not re.match(pattern, phone):
            raise serializers.ValidationError('Invalid phone number')

        return phone


class UserPhoneVerifySerializer(serializers.Serializer):
    code = serializers.IntegerField()
