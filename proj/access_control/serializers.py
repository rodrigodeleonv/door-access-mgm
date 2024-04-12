from rest_framework import serializers
from . import models


class RFIDTagSerializer(serializers.ModelSerializer):
    created_by = serializers.SlugRelatedField(read_only=True, slug_field="first_name")

    class Meta:
        model = models.RFIDTag
        fields = "__all__"

    def to_representation(self, instance: "RFIDTagSerializer"):
        """Represent the field "created_by" as first and last name.

        created_by = "First_Name Last_Name" instead of id or email.
        """
        representation = super().to_representation(instance)
        representation["created_by"] = (
            f"{instance.created_by.first_name} {instance.created_by.last_name}"
        )
        return representation


class AccessControlSerializer(serializers.Serializer):
    tag_id = serializers.CharField()
