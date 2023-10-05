from scrapy import Spider
from scrapy.selector import Selector

from stack.items import StackItem
class StackSpider(Spider):
    name = 'stack'
    allowed_domains = ['github.com']
    start_urls = ['https://github.com/mcauthon471?tab=repositories&q=&type=public&language=&sort=']

    def parse(self, response):
        questions = Selector(response).xpath('//div[@id="user-repositories-list"]/ul/li/div[1]/div[1]/h3')

        for question in questions:
            item = StackItem()
            item['title'] = question.xpath('a/text()').extract()[0]
            item['title'] = item['title'].replace('\n', '').replace(' ', '')
            item['url'] = self.allowed_domains[0] + question.xpath('a/@href').extract()[0]
            yield item
