import scrapy
from itemloaders.processors import MapCompose, TakeFirst, Join
from w3lib.html import remove_tags


def clean_text(text):
    return text.strip()


class ZommitItem(scrapy.Item):
    title = scrapy.Field(
        input_processor=MapCompose(remove_tags, clean_text),
        output_processor=TakeFirst(),
    )
    body = scrapy.Field(
        input_processor=MapCompose(remove_tags, clean_text), output_processor=Join("\n")
    )
    source = scrapy.Field(output_processor=TakeFirst())
    tag = scrapy.Field(output_processor=TakeFirst())
