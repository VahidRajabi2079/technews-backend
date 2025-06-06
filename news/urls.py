from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'news'

router = DefaultRouter()
router.register("tags", views.TagViewSwt, basename='tag')
router.register("", views.NewsViewSet, basename='news')

urlpatterns = router.urls