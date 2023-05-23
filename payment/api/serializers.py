from rest_framework import serializers


class CallbackTransactionSerializer(serializers.Serializer):
    status = serializers.IntegerField()
    track_id = serializers.IntegerField()
    id = serializers.CharField()
    order_id = serializers.CharField()
    amount = serializers.IntegerField()
    hashed_card_no = serializers.CharField()
    date = serializers.IntegerField()
