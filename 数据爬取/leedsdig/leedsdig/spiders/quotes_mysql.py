import scrapy
from leedsdig.items import Article

class QuotesMysqlSpider(scrapy.Spider):
    name = "quotes_mysql"

    start_urls = [
        "https://www.111.com.cn/",
    ]

    def parse(self, response):
        quotes_list = response.css("div.quote")

        item = Article()

        for quote in quotes_list:
            text = quote.css("span.text::text").get()
            item['通用名称'] = text

            function = quote.css("small.author::text").get()
            item['主要功能'] = function

            tags = quote.css("div.tags a.tag::text").getall()
            item['性状'] = ",".join(tags)
            
            yield item
