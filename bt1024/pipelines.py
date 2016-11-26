# -*- coding: utf-8 -*-
import scrapy
import pymongo
import time
import base64
from urllib.parse import urlencode
from scrapy.pipelines.files import FilesPipeline
from scrapy.exceptions import DropItem


class BtPipeline(object):
    def process_item(self, item, spider):
        if item['hash']:
            return item
        else:
            raise DropItem('Missing bt hash in %s' % item)


class TorrentsPipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        timestamp = int(time.time())
        rref = base64.b64encode(str(timestamp).encode(encoding='utf-8'))
        query = urlencode({
            'ref': item['hash'],
            'rref': rref,
            'submit': 'download'
        })
        item['file_urls'] = ['http://www.rmdown.com/download.php?' + query]
        for file_url in item['file_urls']:
            yield scrapy.Request(url=file_url,
                                 headers={'User-Agent': 'Mozilla/5.0',
                                          'Referer': item['bt_url']})


class MongoPipeline(object):
    """将数据存储到MongoDB中，数据库的相关设置在settings.py中"""
    collection_name = 'torrents'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.db[self.collection_name].drop()

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert(dict(item))
        return item