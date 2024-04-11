from rest_framework import permissions, viewsets

from . import models, serializers


class RFIDTagViewSet(viewsets.ModelViewSet):
    queryset = models.RFIDTag.objects.select_related("created_by").order_by("tag_id")
    serializer_class = serializers.RFIDTagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
