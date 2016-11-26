# -*- coding: utf-8 -*-
import scrapy
from bt1024.items import Bt1024Item
from scrapy.linkextractors import LinkExtractor


class BTSpider(scrapy.Spider):
    name = 'bt'

    domain = 'http://www.t66y.com/'

    def start_requests(self):
        n = int(getattr(self, 'n', 5))
        urls = [
            'http://www.t66y.com/thread0806.php?fid=' + fid + '&page=' + str(page)
            for fid in ['2', '15', '17', '18']
            for page in range(2, 2+n)
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        category = response.xpath('//table[@id="ajaxtable"]/tr[1]/th/a[4]/text()').extract_first()
        items = response.xpath('//table[@id="ajaxtable"]//tr[@class="tr3 t_one"]')
        for item in items:
            title = item.xpath('td[@style]/h3/a/text()').extract_first()
            url = item.xpath('td[@style]/h3/a/@href').extract_first()
            date = item.xpath('td[3]/div/text()').extract_first()
            comments = item.xpath('td[4]/text()').extract_first()

            bt = Bt1024Item()
            bt['category'] = category
            bt['date'] = date
            bt['comments'] = comments
            bt['title'] = title
            bt['url'] = self.domain + url

            request = scrapy.Request(bt['url'], callback=self.parse_hash)
            request.meta['bt'] = bt
            yield request

    def parse_hash(self, response):
        link_extractor = LinkExtractor(allow=('.*?rmdown.*?', '.*?xunfs.*?'))
        links = link_extractor.extract_links(response)
        link = links[0].text if len(links) > 0 else ''
        hash = link.split('hash=')[1] if len(link) > 0 else ''

        bt = response.meta['bt']
        bt['hash'] = hash
        bt['bt_url'] = link

        yield bt