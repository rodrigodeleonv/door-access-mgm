from rest_framework import serializers
from . import models


# class RFIDTagSerializer(serializers.HyperlinkedModelSerializer):
class RFIDTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RFIDTag
        fields = '__all__'
