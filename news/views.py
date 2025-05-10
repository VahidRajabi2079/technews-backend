from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from . import models,serializers


class TagViewSwt(ModelViewSet):
    serializer_class = serializers.TagSerializer
    queryset = models.Tag.objects.all()


class NewsViewSet(ModelViewSet):
    serializer_class = serializers.NewsSerializer
    queryset = models.News.objects.all()
