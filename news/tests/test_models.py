import pytest
from news.models import Tag, News


@pytest.fixture
def tag_python():
    return Tag.objects.create(name="Python")


@pytest.fixture
def tag_django():
    return Tag.objects.create(name="Django")


@pytest.mark.django_db
def test_create_tag(tag_python):
    assert Tag.objects.count() == 1
    assert tag_python.name == "Python"


@pytest.mark.django_db
def test_str_method(tag_django):
    assert str(tag_django) == "Django"


@pytest.mark.django_db
def test_cannot_create_duplicate_tag(tag_python):
    with pytest.raises(Exception):
        Tag.objects.create(name="Python")


@pytest.fixture
def sample_news():
    return News.objects.create(
        title="Test News",
        body="This is a test body",
        source="BBC"
    )


@pytest.fixture
def tags():
    return [Tag.objects.create(name="Tech"), Tag.objects.create(name="AI")]


@pytest.mark.django_db
def test_create_news(sample_news):
    assert News.objects.count() == 1
    assert sample_news.title == "Test News"
    assert sample_news.body == "This is a test body"
    assert sample_news.source == "BBC"
    assert sample_news.datatime_created is not None
    assert sample_news.datatime_modified is not None


@pytest.mark.django_db
def test_str_method_news(sample_news):
    assert str(sample_news) == "Test News"


@pytest.mark.django_db
def test_add_tags_to_news(sample_news, tags):
    sample_news.tags.set(tags)
    assert sample_news.tags.count() == 2
    for tag in tags:
        assert tag in sample_news.tags.all()


@pytest.mark.django_db
def test_deleting_news_does_not_delete_tags(sample_news, tags):
    sample_news.tags.set(tags)
    sample_news.delete()
    assert Tag.objects.count() == 2


@pytest.mark.django_db
def test_deleting_tag_does_not_delete_news(sample_news, tags):
    sample_news.tags.set(tags)
    tags[0].delete()
    assert News.objects.count() == 1
    assert sample_news.tags.count() == 1


@pytest.mark.django_db
def test_update_news(sample_news):
    sample_news.title = "Updated Title"
    sample_news.save()
    sample_news.refresh_from_db()
    assert sample_news.title == "Updated Title"


@pytest.mark.django_db
def test_clear_tags_from_news(sample_news, tags):
    sample_news.tags.set(tags)
    sample_news.tags.clear()
    assert sample_news.tags.count() == 0


@pytest.mark.django_db
def test_datetime_fields(sample_news):
    assert sample_news.datatime_created <= sample_news.datatime_modified


@pytest.mark.django_db
def test_add_tag_after_creation(sample_news):
    new_tag = Tag.objects.create(name="Science")
    sample_news.tags.add(new_tag)
    assert new_tag in sample_news.tags.all()