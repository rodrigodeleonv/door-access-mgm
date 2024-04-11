import logging
from rest_framework import permissions, viewsets, status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView

from . import models, serializers


# from rest_framework.viewsets import ViewSet
# from rest_framework.decorators import action
from users.models import User

logger = logging.getLogger(__name__)


class RFIDTagViewSet(viewsets.ModelViewSet):
    """Query optimized with select_related."""

    queryset = models.RFIDTag.objects.select_related("created_by").order_by("tag_id")
    serializer_class = serializers.RFIDTagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# class AccessControlViewSet(ViewSet):
#     """Viewset for access control."""

#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#     serializer_class = serializers.AccessControlSerializer
#     # queryset = models.RFIDTag.objects.all()

#     @action(detail=False, methods=["get"])
#     def verify_tag(self, request):
#         """Get all tags."""
#         # tags = None
#         # serializer = serializers.RFIDTagSerializer(tags, many=True)
#         # return Response(serializer.data)
#         return Response(None)


class AccessDoor(APIView):
    """ """

    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAdminUser]
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    permission_classes = [permissions.AllowAny]

    def get(self, request: Request):
        """Temporal."""
        usernames = [user.email for user in User.objects.all()]
        return Response(usernames)

    def post(self, request: Request):
        """Process Tag ID in order to grant access."""
        tag_id = request.data.get("tag_id")
        logger.debug(f"Tag ID received: {tag_id}")
        try:
            models.RFIDTag.objects.get(tag_id="123456789")
        except models.RFIDTag.DoesNotExist:
            return Response(
                {"message": f"Tag ID: {tag_id} not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        #
        # TODO: Process Tag ID to grant access
        #
        return Response(
            {"message": f"Tag ID: {tag_id} received successfully"},
            status=status.HTTP_201_CREATED,
        )
