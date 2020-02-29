# -*- coding: utf-8 -*-
import scrapy


class FundEastmoneySpider(scrapy.Spider):
    name = 'fund.eastmoney'
    allowed_domains = ['fund.eastmoney.com']
    start_urls = ['http://fund.eastmoney.com/']

    def parse(self, response):
        pass
