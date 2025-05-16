import sys
import os
import django
from django.db import IntegrityError, transaction
from twisted.internet.threads import deferToThread


sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()


from news.models import News, Tag


class SaveNewsToDjangoPipeline:
    def process_item(self, item, spider):
        return deferToThread(self.save_item, item, spider)

    def save_item(self, item, spider):
        spider.logger.info(f"Processing item: {item.get('title')}")
        try:
            with transaction.atomic():
                news_obj, created = News.objects.get_or_create(
                    title=item["title"],
                    source=item["source"],
                    defaults={"body": item["body"]},
                )
                tag_name = item.get("tag")
                if tag_name:
                    tag_obj, _ = Tag.objects.get_or_create(name=tag_name)
                    news_obj.tags.add(tag_obj)
                    news_obj.save()

        except IntegrityError as e:
            spider.logger.error(f"IntegrityError: {e}")
        except Exception as e:
            spider.logger.error(f"Unexpected error: {e}")
        return item
