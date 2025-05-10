from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class News(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    tags = models.ManyToManyField(Tag, related_name="news")
    source = models.CharField(max_length=255)
    datatime_created = models.DateTimeField(auto_now_add=True)
    datatime_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
