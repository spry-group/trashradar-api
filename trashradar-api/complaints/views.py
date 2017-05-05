from rest_framework import permissions, status, viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

import cloudinary
import cloudinary.uploader
import cloudinary.api
from django.conf import settings

from accounts.permissions import IsReadOnly
from complaints import models, serializers


class ComplaintViewSet(viewsets.ModelViewSet):
    queryset = models.Complaint.objects.all()
    serializer_class = serializers.ComplaintSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    cloudinary.config(
        cloud_name=settings.CLOUDINARY_CLOUD_NAME,
        api_key=settings.CLOUDINARY_API_KEY,
        api_secret=settings.CLOUDINARY_API_SECRET,
    )

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            saved_image = cloudinary.uploader.upload(request.data.get('picture'))
            url = saved_image.get('url', None)
            if url:
                picture = url
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({
            'status': 'Bad Request',
            'message': 'Request failed validation.',
            'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def confirm(self, request, pk):
        complaint = self.get_object()
        complaint.counter += 1
        complaint.save()
        return Response({}, status.HTTP_204_NO_CONTENT)

    @detail_route(methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def clean(self, request, pk):
        complaint = self.get_object()
        complaint.current_state = 2
        complaint.save()
        return Response({}, status.HTTP_204_NO_CONTENT)


class EntityViewSet(viewsets.ModelViewSet):
    queryset = models.Entity.objects.all()
    serializer_class = serializers.EntitySerializer
    permission_classes = (IsReadOnly,)
