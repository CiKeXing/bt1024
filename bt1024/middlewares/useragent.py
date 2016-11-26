# -*- coding: utf-8 -*-
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from bt1024.fake_useragent import UserAgent


class RandomUserAgentMiddleware(UserAgentMiddleware):
    ua = UserAgent()

    def process_request(self, request, spider):
        request.headers.setdefault(b'User-Agent', self.ua.random)
