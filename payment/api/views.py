from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status

from .import serializers

class CallbackTransactionView(generics.GenericAPIView):
    serializer_class = serializers.CallbackTransactionSerializer

    def post(self, request):
        callback_serializer = self.serializer_class(data=request.data)
        if callback_serializer.is_valid(raise_exception=True):
            return Response(
                data=callback_serializer.data,
                status=status.HTTP_501_NOT_IMPLEMENTED
            )
