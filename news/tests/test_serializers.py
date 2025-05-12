import pytest
from news.models import Tag, News
from news.serializers import TagSerializer, NewsSerializer


@pytest.mark.django_db
def test_tag_serializer():
    tag = Tag.objects.create(name="Python")
    serializer = TagSerializer(tag)
    assert serializer.data == {"id": tag.id, "name": "Python"}


@pytest.mark.django_db
def test_news_serializer_read():
    tag1 = Tag.objects.create(name="Tech")
    tag2 = Tag.objects.create(name="AI")
    news = News.objects.create(title="Test News", body="Body", source="BBC")
    news.tags.set([tag1, tag2])

    serializer = NewsSerializer(news)
    data = serializer.data

    assert data["title"] == "Test News"
    assert data["body"] == "Body"
    assert data["source"] == "BBC"
    assert len(data["tags"]) == 2
    assert data["tags"][0]["name"] in ["Tech", "AI"]
    assert "tag_ids" not in data  # چون write_only است


@pytest.mark.django_db
def test_news_serializer_write():
    tag1 = Tag.objects.create(name="Tech")
    tag2 = Tag.objects.create(name="AI")

    data = {
        "title": "New Article",
        "body": "Some body",
        "source": "CNN",
        "tag_ids": [tag1.id, tag2.id],
    }

    serializer = NewsSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    news = serializer.save()

    assert news.title == "New Article"
    assert news.tags.count() == 2
    assert tag1 in news.tags.all()


@pytest.mark.django_db
def test_news_serializer_update():
    tag1 = Tag.objects.create(name="Tech")
    tag2 = Tag.objects.create(name="AI")
    tag3 = Tag.objects.create(name="Python")

    news = News.objects.create(title="Old Title", body="Old Body", source="BBC")
    news.tags.set([tag1])

    data = {
        "title": "Updated Title",
        "body": "Updated Body",
        "source": "Al Jazeera",
        "tag_ids": [tag2.id, tag3.id],
    }

    serializer = NewsSerializer(news, data=data)
    assert serializer.is_valid(), serializer.errors
    updated_news = serializer.save()

    assert updated_news.title == "Updated Title"
    assert updated_news.body == "Updated Body"
    assert updated_news.source == "Al Jazeera"
    assert tag2 in updated_news.tags.all()
    assert tag3 in updated_news.tags.all()
    assert tag1 not in updated_news.tags.all()
