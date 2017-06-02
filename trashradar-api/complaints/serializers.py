from rest_framework import serializers

from complaints.models import Complaint, Entity


class ComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = (
            'id', 'owner', 'location', 'entity', 'picture', 'counter', 'current_state', 'tweet_status'
        )
        extra_kwargs = {
            'picture': {'read_only': True},
        }


class EntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entity
        fields = (
            'id', 'name', 'twitter', 'phone'
        )
