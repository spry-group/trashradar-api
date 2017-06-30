import cloudinary
import cloudinary.uploader
import cloudinary.api

from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_gis.serializers import GeoModelSerializer

from complaints.models import Complaint, Entity
from utils.tasks.share import share_complaint


class ComplaintSerializer(GeoModelSerializer):
    cloudinary.config(
        cloud_name=settings.CLOUDINARY_CLOUD_NAME,
        api_key=settings.CLOUDINARY_API_KEY,
        api_secret=settings.CLOUDINARY_API_SECRET,
    )

    class Meta:
        model = Complaint
        fields = (
            'id', 'owner', 'location', 'entity', 'picture', 'counter', 'current_state'
        )
        extra_kwargs = {
            'picture': {'read_only': True},
        }

    def create(self, validated_data):
        request = self.context.get('request')
        saved_image = cloudinary.uploader.upload(request.data.get('picture'))
        url = saved_image.get('url', None)
        if not url:
            raise ValidationError({'picture': 'Image was not uploaded to cloudinary.'})

        validated_data['picture'] = url
        complaint = super(ComplaintSerializer, self).create(validated_data)
        share_complaint.delay(complaint.pk)
        return complaint

    def validate(self, data):
        request = self.context.get('request')
        picture = request.data.get('picture')
        if not picture or not hasattr(picture, 'read'):
            raise ValidationError({'picture': 'Image is required.'})
        return data


class EntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entity
        fields = (
            'id', 'name', 'twitter', 'phone'
        )
