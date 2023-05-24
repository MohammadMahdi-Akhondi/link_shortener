from django.shortcuts import get_object_or_404, redirect
from django.db import transaction
from rest_framework import generics
from decouple import config
import datetime

from .import serializers
from ..models import Transaction
from ..idpay import IDPayAPI

class CallbackTransactionView(generics.GenericAPIView):
    serializer_class = serializers.CallbackTransactionSerializer

    def post(self, request):
        callback_serializer = self.serializer_class(data=request.data)
        if callback_serializer.is_valid(raise_exception=True):
            valid_data = callback_serializer.validated_data
            current_transaction = get_object_or_404(
                Transaction, order_id=valid_data.get('order_id'),
                transaction_id = valid_data.get('id'), status = 8,
            )
            date = datetime.datetime.fromtimestamp(valid_data.get('date'))
            current_transaction.status = valid_data.get('status')
            current_transaction.gateway_track_id = valid_data.get('track_id')
            current_transaction.card_number = valid_data.get('hashed_card_no')
            current_transaction.date = date
            current_transaction.save()
            api = IDPayAPI(
                apikey=config('IDPAY_API_KEY', default='6a7f99eb-7c20-4412-a972-6dfb7cd253a4'),
                sandbox=config('IDPAY_SANDBOX'),
            )
            data = {
                'id': current_transaction.transaction_id,
                'order_id': current_transaction.order_id,
            }
            if current_transaction.status == 10:
                response = api.confirm_transaction(data)
                duration = datetime.timedelta(days=30)
                with transaction.atomic():
                    current_transaction.status = response.get('status')
                    current_transaction.bank_track_id = response.get('payment').get('track_id')
                    current_transaction.save()
                    current_transaction.user.premium_until = datetime.datetime.now() + duration
                    current_transaction.user.save()

            return redirect('link:list_link')
