import scrapy
from urllib.parse import urlparse
from scrapy.loader import ItemLoader
from zommit.items import ZommitItem  
from w3lib.html import remove_tags


class ZommitSpiderSpider(scrapy.Spider):
    name = "zommit_spider"
    allowed_domains = ["zoomit.ir"]
    start_urls = ["https://www.zoomit.ir/tech/"]

    def parse(self, response):
        for link in response.css("a.cursor-pointer::attr(href)").getall():
            if link and link.startswith("https://www.zoomit.ir"):
                yield response.follow(link, callback=self.parse_news)

    def parse_news(self, response):
        loader = ItemLoader(item=ZommitItem(), response=response)

        loader.add_css("title", "h1.sc-9996cfc-0::text")
        loader.add_css("body", "div.sc-481293f7-1 p::text")
        loader.add_value("source", response.url)

        path = urlparse(response.url).path
        tag = path.strip("/").split("/")[0]
        loader.add_value("tag", tag)

        yield loader.load_item()
