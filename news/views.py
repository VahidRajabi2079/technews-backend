from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAdminUser



from . import models, permissions, serializers, filters, pagination


class TagViewSwt(ModelViewSet):
    serializer_class = serializers.TagSerializer
    queryset = models.Tag.objects.all().order_by('-id')
    pagination_class = pagination.DefaultPagination
    # permission_classes = [IsAdminUser]


class NewsViewSet(ModelViewSet):
    serializer_class = serializers.NewsSerializer
    queryset = (
        models.News.objects.all().prefetch_related("tags").order_by("-datatime_modified")
    )
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.NewsFilter
    # permission_classes = [permissions.IsAdminOrReadOnly]
    pagination_class = pagination.DefaultPagination
