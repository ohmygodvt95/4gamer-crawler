import scrapy
from crawler_4gamer.items import Crawler4GamerItem
import json
import re


TAG_RE = re.compile(r'<[^>]+>')


class GamerSpider(scrapy.Spider):
    name = 'gamer'
    allowed_domains = ['4gamer.net']
    start_urls = ['https://www.4gamer.net/']
    categories = [
        {
            'title': 'TS019',
            'pages': 481,
            'category': 'PC'
        },
        {
            'title': 'TS001',
            'pages': 410,
            'category': 'Android'
        },
        {
            'title': 'TS013',
            'pages': '529',
            'category': 'iPhone'
        }
    ]
    custom_settings = {
        'FEEDS': {
            f'output.csv': {
                'format': 'csv',
                'overwrite': True
            }
        }
    }
    search_url = 'https://www.4gamer.net/script/search/search.php'

    def start_requests(self):
        for category in self.categories:
            for i in range(1, category['pages'] + 1):
                referer_url = "https://www.4gamer.net/script/search/index.php?mode=title&" + category['title']
                form_data = {'PAGE': str(i), 'KEYWORD_IDS': category['title'], 'SEARCH_TYPE': 'list', 'MODE': 'title'}
                yield scrapy.FormRequest(self.search_url, formdata=form_data, callback=self.parse, headers={'Referer': referer_url}, cb_kwargs={'category': category['category']})

    def parse(self, response, category):
        body = response.body.decode('EUC-JP')
        m = re.findall("<h2>(.+)</h2>", body)
        for c in m:
            item = Crawler4GamerItem(category=category, title=self.remove_tags(c))
            yield item

    def remove_tags(self, text):
        return TAG_RE.sub('', text)
