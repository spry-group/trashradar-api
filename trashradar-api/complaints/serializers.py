from rest_framework import serializers

from complaints.models import Complaint, Entity


class ComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = (
            'id', 'owner', 'entity', 'location', 'picture', 'counter', 'current_state'
        )


class EntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entity
        fields = (
            'id', 'name', 'twitter', 'phone'
        )
