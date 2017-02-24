from rest_framework import serializers

from complaints.models import Entity


class EntitySerializer(serializers.ModelSerializer):
    """
    Entity Serializer
    """
    class Meta:
        model = Entity
        fields = (
            'id', 'name', 'twitter', 'phone'
        )
