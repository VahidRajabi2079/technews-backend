import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from news.models import Tag, News

pytestmark = pytest.mark.django_db


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def tag():
    return Tag.objects.create(name="Tech")


@pytest.fixture
def news(tag):
    news_obj = News.objects.create(
        title="AI Revolution",
        body="Something about AI.",
        source="TechCrunch",
    )
    news_obj.tags.add(tag)
    return news_obj


# ----------------- TAG TESTS -----------------

def test_list_tags(api_client, tag):
    url = reverse("news:tag-list")
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data["results"][0]["name"] == tag.name


def test_create_tag(api_client):
    url = reverse("news:tag-list")
    response = api_client.post(url, {"name": "Science"})
    assert response.status_code == 201
    assert Tag.objects.filter(name="Science").exists()


def test_retrieve_tag(api_client, tag):
    url = reverse("news:tag-detail", args=[tag.id])
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data["name"] == tag.name


def test_update_tag(api_client, tag):
    url = reverse("news:tag-detail", args=[tag.id])
    response = api_client.put(url, {"name": "Updated Tag"})
    assert response.status_code == 200
    tag.refresh_from_db()
    assert tag.name == "Updated Tag"


def test_delete_tag(api_client, tag):
    url = reverse("news:tag-detail", args=[tag.id])
    response = api_client.delete(url)
    assert response.status_code == 204
    assert Tag.objects.count() == 0


# ----------------- NEWS TESTS -----------------

def test_list_news(api_client, news):
    url = reverse("news:news-list")
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data["results"][0]["title"] == news.title


def test_create_news(api_client, tag):
    url = reverse("news:news-list")
    data = {
        "title": "New Article",
        "body": "Some content",
        "source": "CNN",
        "tag_ids": [tag.id],
    }
    response = api_client.post(url, data, format="json")
    assert response.status_code == 201
    assert News.objects.filter(title="New Article").exists()


def test_retrieve_news(api_client, news):
    url = reverse("news:news-detail", args=[news.id])
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data["title"] == news.title


def test_update_news(api_client, news):
    url = reverse("news:news-detail", args=[news.id])
    data = {
        "title": "Updated News",
        "body": news.body,
        "source": news.source,
        "tag_ids": [tag.id for tag in news.tags.all()],
    }
    response = api_client.put(url, data, format="json")
    assert response.status_code == 200
    news.refresh_from_db()
    assert news.title == "Updated News"


def test_delete_news(api_client, news):
    url = reverse("news:news-detail", args=[news.id])
    response = api_client.delete(url)
    assert response.status_code == 204
    assert News.objects.count() == 0
