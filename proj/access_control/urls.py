from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"tag", views.RFIDTagViewSet)
# router.register(r"access_control", views.AccessControlViewSet, basename="access_control")

urlpatterns = [
    path("", include(router.urls)),
    path("verify_tag/", views.AccessDoor.as_view(), name="verify_tag-get"),
]
