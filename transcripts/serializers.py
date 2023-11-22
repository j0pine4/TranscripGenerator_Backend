from rest_framework import serializers
from . import models

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Document
        fields = [
            'id',
            'user',
            'videoID',
            'title',
            'description',
            'content',
            'type',
            'created_on',
            'last_modified',
        ]

class DocumentThumbnailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Document
        fields = [
            'id',
            'videoID',
            'title',
            'description',
            'created_on',
        ]

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Message
        fields = "__all__"

