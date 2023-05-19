from rest_framework import serializers

from ..models import Link

class CreateLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = (
            'title',
            'real_link',
            'description',
            'is_active',
            'expire_at',
        )


class ListLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = '__all__'


class UpdateLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        exclude = (
            'id',
            'user',
            'created_at',
            'updated_at',
            'deleted_at',
            'clicks_count',
        )
