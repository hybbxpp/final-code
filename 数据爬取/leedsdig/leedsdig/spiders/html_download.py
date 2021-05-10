import scrapy

class HtmlDownloadSpider(scrapy.Spider):
    name = "html_download"

    def start_requests(self):
        urls = [
            "https://www.111.com.cn/",
        ]

        for url in urls:
            yield scrapy.Request(url, callback=self.download)

    
    def download(self, response):
        page = response.url.split("/")[-2]
        filename = "quotes-%s.html" % page

        with open(filename, "wb") as f:
            f.write(response.body)

        self.log("saved file %s" % filename)
