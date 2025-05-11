from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAdminUser
from rest_framework.pagination import PageNumberPagination
from rest_framework_tracking.mixins import LoggingMixin

from . import models, serializers, filters, permisions


class TagViewSwt(LoggingMixin, ModelViewSet):
    serializer_class = serializers.TagSerializer
    queryset = models.Tag.objects.all()
    pagination_class = PageNumberPagination
    PageNumberPagination.page_size = 10
    # permission_classes = [IsAdminUser]


class NewsViewSet(LoggingMixin, ModelViewSet):
    serializer_class = serializers.NewsSerializer
    queryset = (
        models.News.objects.all().prefetch_related("tags").order_by("-datatime_modified")
    )
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.NewsFilter
    # permission_classes = [permisions.IsAdminOrReadOnly]
    pagination_class = PageNumberPagination
    PageNumberPagination.page_size = 2
