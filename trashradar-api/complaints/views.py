from rest_framework import permissions, status, viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from accounts.permissions import IsReadOnly
from complaints import models, serializers


class ComplaintViewSet(viewsets.ModelViewSet):
    queryset = models.Complaint.objects.all()
    serializer_class = serializers.ComplaintSerializer
    permission_classes = (IsReadOnly,)

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
