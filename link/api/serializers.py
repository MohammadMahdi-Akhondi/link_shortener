from rest_framework import serializers

from ..models import Link

class CreateLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        exclude = (
            'user',
            'token',
            'clicks_count',
            'deleted_at',
        )
