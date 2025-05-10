from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend

from . import models,serializers,filters


class TagViewSwt(ModelViewSet):
    serializer_class = serializers.TagSerializer
    queryset = models.Tag.objects.all()


class NewsViewSet(ModelViewSet):
    serializer_class = serializers.NewsSerializer
    queryset = models.News.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.NewsFilter



    