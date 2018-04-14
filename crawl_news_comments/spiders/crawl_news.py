# -*- coding: utf-8 -*-
from scrapy.spiders import Spider
from scrapy.http import Request
from scrapy.selector import Selector
from crawl_news_comments.items import NewsItem
from crawl_news_comments.spiders.func import getHTMLText,ListCombiner
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import requests
import re
import json

class CrawlNewsSpider(CrawlSpider):
    name = 'crawl_news'
    allowed_domains = ['new.qq.com','news.qq.com']
    start_urls = [ 'http://news.qq.com']

    url_pattern1= r'(.*)/a/(\d{8})/(\d+)\.htm'
    url_pattern2=r'(.*)/omn/(.+)\.html'
    url_pattern3=r'(.*)/omn/([A-Z0-9]{16,19})'
    url_pattern4=r'(.*)/omn/(\d{8})/(.+)\.html'
    rules = (
        Rule(LinkExtractor(allow=(url_pattern1)),'parse_news1'),
        Rule(LinkExtractor(allow=(url_pattern2)),'parse_news2'),
        Rule(LinkExtractor(allow=(url_pattern3)),'parse_news3'),
    )

    def parse_news1(self, response):
        sel = Selector(response)
        print(response.url)
        pattern = re.match(self.url_pattern1, str(response.url))
        item = NewsItem()
        item['source'] = 'tencent'#pattern.group(1)
        item['date'] = pattern.group(2)
        item['newsId'] = pattern.group(3)
        item['cmtId'] = (sel.re(r"cmt_id = (.*);"))[0] # unicode string
        item['comments'] = {'link':str('http://coral.qq.com/')+item['cmtId']}
        item['contents'] = {'link':str(response.url), 'title':u'', 'passage':u''}
        item['contents']['title'] = sel.xpath('//h1/text()').extract()[0]
        item['contents']['passage'] = ListCombiner(sel.xpath('//p/text()').extract())
        return item


    def parse_news2(self,response):
        sel = Selector(response)
        pattern = re.match(self.url_pattern4, str(response.url))
        item=NewsItem()
        item['source'] = 'tencent'#pattern.group(1)
        item['date'] = pattern.group(2)
        item['newsId'] = pattern.group(3)
        item['cmtId'] = (sel.re(r"\"comment_id\":\"(\d*)\","))[0]
        item['comments'] = {'link':str('http://coral.qq.com/')+item['cmtId']}
        item['contents'] = {'link':str(response.url), 'title':u'', 'passage':u''}
        item['contents']['title'] = sel.xpath('//h1/text()').extract()[0]
        item['contents']['passage'] = ListCombiner(sel.xpath('//p/text()').extract())
        return item

    def parse_news3(self,response):
        item = NewsItem()
        print(response.url)
        str1='http://openapi.inews.qq.com/getQQNewsNormalContent?id='
        str2='&chlid=news_rss&refer=mobilewwwqqcom&otype=jsonp&ext_data=all&srcfrom=newsapp&callback=getNewsContentOnlyOutput'
        pattern = re.match(self.url_pattern3, str(response.url))
        date=re.search(r"(\d{8})",pattern.group(2))#匹配时间
        item['source'] = 'tencent'#pattern.group(1)
        item['date'] = date.group(0)
        item['newsId'] = pattern.group(2)
        print(pattern.group(2))
        out=getHTMLText(str1+pattern.group(2)+str2)
        g=re.search("getNewsContentOnlyOutput\\((.+)\\)", out)
        out=json.loads(g.group(1))
        item['cmtId'] =out["cid"]
        item['comments'] = {'link':str('http://coral.qq.com/')+item['cmtId']}
        item['contents'] = {'link':str(response.url), 'title':u'', 'passage':u''}
        item['contents']['title'] = out["title"]
        item['contents']['passage'] =out["ext_data"]["cnt_html"]
        return item
