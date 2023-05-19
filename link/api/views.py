from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status, generics
from django.utils import timezone
from django.shortcuts import get_object_or_404
import uuid

from . import serializers
from ..models import Link
from .. import messages
from ..permissions import IsOwnerOrAdmin


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
                status=status.HTTP_201_CREATED,
            )


class ListLinkView(generics.ListAPIView):
    """
    View for list links for the authenticated user.
    """
    authentication_classes = (JWTAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = serializers.ListLinkSerializer

    def get_queryset(self):
        return Link.objects.filter(user=self.request.user, deleted_at__isnull=True)


class UpdateLinkView(generics.UpdateAPIView):
    """
    View for update links for the authenticated user.
    """
    authentication_classes = (JWTAuthentication, )
    permission_classes = (IsOwnerOrAdmin, )
    serializer_class = serializers.UpdateLinkSerializer

    def get_object(self):
        link_id = self.kwargs.get('link_id')
        link = get_object_or_404(Link, pk=link_id, deleted_at__isnull=True)

        # May raise a permission denied
        self.check_object_permissions(self.request, link)
        return link


class DeleteLinkView(generics.DestroyAPIView):
    """
    View for update links for the authenticated user.
    """
    authentication_classes = (JWTAuthentication, )
    permission_classes = (IsOwnerOrAdmin, )
    serializer_class = serializers.UpdateLinkSerializer
    queryset = Link.objects.filter(deleted_at__isnull=True)
    lookup_url_kwarg = 'link_id'

    def perform_destroy(self, link):
        link.deleted_at = timezone.now()
        link.save()
