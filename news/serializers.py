from rest_framework import serializers
from . import models


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = [
            "id",
            "name",
        ]


class NewsSerializer(serializers.ModelSerializer):
    tags = TagSerializer(
        many=True,
        read_only=True,
    )
    tag_ids = serializers.PrimaryKeyRelatedField(
        queryset=models.Tag.objects.all(),
        many=True,
        write_only=True,
    )

    class Meta:
        model = models.News
        fields = [
            "id",
            "title",
            "body",
            "tags",
            "tag_ids",
            "source",
            "datatime_created",
            "datatime_modified",
        ]

    def create(self, validated_data):
        tag_ids = validated_data.pop("tag_ids")
        news = models.News.objects.create(**validated_data)
        news.tags.set(tag_ids)
        return news

    def update(self, instance, validated_data):
        tag_ids = validated_data.pop("tag_ids", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if tag_ids is not None:
            instance.tags.set(tag_ids)
        return instance
