import pytest
from django.urls import reverse, resolve
from rest_framework import status
from rest_framework.test import APIClient
from news import views


@pytest.mark.django_db
class TestURLs:
    client = APIClient()

    def test_tag_list_url(self):
        url = reverse('news:tag-list')
        assert resolve(url).func.cls == views.TagViewSwt
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_news_list_url(self):
        url = reverse('news:news-list')
        assert resolve(url).func.cls == views.NewsViewSet
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_tag_detail_url(self, django_db_setup, django_db_blocker):
        with django_db_blocker.unblock():
            from news.models import Tag
            tag = Tag.objects.create(name="TestTag")
        url = reverse('news:tag-detail', kwargs={'pk': tag.pk})
        assert resolve(url).func.cls == views.TagViewSwt
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_news_detail_url(self, django_db_setup, django_db_blocker):
        with django_db_blocker.unblock():
            from news.models import News
            news = News.objects.create(title="Test", body="Body", source="Source")
        url = reverse('news:news-detail', kwargs={'pk': news.pk})
        assert resolve(url).func.cls == views.NewsViewSet
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
