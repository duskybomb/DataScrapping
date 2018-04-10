import scrapy
class MetroSpider(scrapy.Spider):
    name = "metro"

    start_urls = [
        # Add urls obtained from clean_list.py
    ]

    def parse(self, response):
        filename = response.url.split("/")[-1] + '.html'
        with open(filename, 'wb') as f:
            f.write(response.body)