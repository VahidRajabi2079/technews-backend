from rest_framework import serializers
from . import models


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = ["id", "name"]


class NewsSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(
        slug_field="name", 
        queryset=models.Tag.objects.all(), 
        many=True
    )

    class Meta:
        model = models.News
        fields = ["id", "title", "body", "tags", "source", "datatime_created"]

