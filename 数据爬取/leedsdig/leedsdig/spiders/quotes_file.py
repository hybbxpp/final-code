import scrapy

class QuotesFileSpider(scrapy.Spider):
    name = "quotes_file"

    start_urls = [
        "https://www.111.com.cn/",
    ]

    def parse(self, response):
        quotes_list = response.css("div.quote")

        for quote in quotes_list:
            yield {
                'name': quote.css("span.text::text").get(),
                'function': quote.css("small.author::text").get(),
                'tags': quote.css("div.tags a.tag::text").getall()
            }
            