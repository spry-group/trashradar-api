
from rest_framework import viewsets

from accounts.permissions import IsReadOnly
from complaints import models, serializers


class EntityViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Accounts
    """
    queryset = models.Entity.objects.all()
    serializer_class = serializers.EntitySerializer
    permission_classes = (IsReadOnly,)
