
from rest_framework import viewsets

from accounts.permissions import IsReadOnly
from complaints import models, serializers


class ComplaintViewSet(viewsets.ModelViewSet):
    queryset = models.Complaint.objects.all()
    serializer_class = serializers.ComplaintSerializer
    permission_classes = (IsReadOnly,)


class EntityViewSet(viewsets.ModelViewSet):
    queryset = models.Entity.objects.all()
    serializer_class = serializers.EntitySerializer
    permission_classes = (IsReadOnly,)
