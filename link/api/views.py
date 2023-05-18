from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status, generics
from django.utils import timezone
import uuid

from . import serializers
from ..models import Link
from .. import messages


def generate_unique_token(token_length: int) -> str:
    while True:
        token = uuid.uuid4().hex[:token_length]
        if not Link.objects.filter(token=token, deleted_at__isnull=False).exists():
            return token


class CreateLinkView(generics.GenericAPIView):
    """
    View for creating a new link for the authenticated user.
    """
    authentication_classes = (JWTAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = serializers.CreateLinkSerializer

    def post(self, request):
        """
        According to the level of the user, a unique link is created for him.
        """
        create_serializer = self.serializer_class(data=request.data)
        if create_serializer.is_valid(raise_exception=True):
            token_length = 12
            user = request.user
            if user.premium_until and user.premium_until > timezone.now():
                token_length = 6

            token = generate_unique_token(token_length)
            create_serializer.save(user=user, token=token)

            return Response(
                data={'message': messages.LINK_CREATED},
                status=status.HTTP_200_OK,
            )
