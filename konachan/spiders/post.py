# -*- coding: utf-8 -*-
import scrapy
from scrapy import signals
# from scrapy.xlib.pydispatch import dispatcher
import urllib
from konachan.items import KonachanItem
import logging
import json
import os

class PostSpider(scrapy.Spider):
    name = 'post'
    page = 1
    number = 1
    folder = 'tags-'
    cache = {}
    stopWhenCached = True
    cacheFilePath = '';

    allowed_domains = ['konachan.com']

    def start_requests(self):
        url = 'https://konachan.com/post'
        arg = getattr(self, 'tag', None)
        if arg is not None:
            self.log('Request tags = ' + arg, logging.INFO)
            tags = arg.split(' ')
            for t in tags:
                t = urllib.parse.quote_plus(t)
            tagsStr = '+'.join(tags)
            url = url + '?tags=' + tagsStr
            self.folder = self.folder + tagsStr
        else:
            self.log('No request tag', logging.INFO)
            self.folder = self.folder + 'default'
        cwd = os.getcwd()
        self.cacheFilePath = os.path.join(cwd, 'cache', self.folder + '.json')


        # if stop argument is false, just skip download, or close spider
        shouldStop = getattr(self, 'stop', None)
        if shouldStop is not None:
            self.log('Stop when cached = ' + shouldStop, logging.INFO)
            if shouldStop == 'false':
                self.stopWhenCached = False

        self.cache = self.read_cache()
        folder = self.cache.get(self.folder)
        if folder is None:
            folder = self.cache[self.folder] = {}

        # if clear
        shouldClear = getattr(self, 'clear', None)
        if shouldClear is not None:
            if  shouldClear == 'true':
                self.cache[self.folder] = {};
                self.log('Clear cache', logging.INFO)

        yield scrapy.Request(url, self.parse)
        

    def parse(self, response):
        posts = response.css('a.thumb::attr(href)').getall()
        for post in posts:
            if post is not None:
                self.log('try to load page ' + str(self.page) + ', number ' + str(self.number), logging.INFO)
                s = post.split('/')
                id = s[len(s) - 2]
                folder = self.cache[self.folder]
                cache = folder.get(id)
                if cache is not None:
                    if self.stopWhenCached == True:
                        self.log('Post already exist, close', logging.INFO)
                        self.close(self, 'Post already download, close')
                        return
                    else:
                        self.log('Post already exist, skip', logging.INFO)
                        yield None
                        continue
                else:
                    self.cache[self.folder][id] = True
                yield response.follow(response.urljoin(post), callback=self.parsePostDetail)
                self.number = self.number + 1
        self.page = self.page + 1
        next = response.css('a.next_page::attr(href)')
        if next is not None:
            yield response.follow(response.urljoin(next.get()), callback=self.parse)
        else:
            self.write_cache(self.cache)
    
    def parsePostDetail(self, response):
        url = response.request.url
        s = response.request.url.split('/')
        id = s[len(s) - 2]
        post = KonachanItem()
        post['id'] = id
        links = response.css('li.tag-link a::text').getall()
        tag = [];
        i = len(links)
        for link in links:
            if link is not None and link != '?':
                tag.append(link)
        post['tag'] = ','.join(tag)
        post['folder'] = self.folder
        png = response.css('#png::attr(href)').extract_first()
        if png is not None:
            self.log('Found png, tags are ' + post['tag'], logging.INFO)
            post['file_urls'] = [png]
            yield post
            return
        jpg = response.css('#highres::attr(href)').extract_first()
        if jpg is not None:
            self.log('Found jpg, tags are ' + post['tag'], logging.INFO)
            post['file_urls'] = [jpg]
            yield post
            return
        yield None

    # Download picture by path
    def read_cache(self):
        cacheDir = os.path.join(os.getcwd(), 'cache')
        if os.path.isdir(cacheDir):
            if os.path.isfile(self.cacheFilePath):
                with open(self.cacheFilePath) as f:
                    data = json.load(f)
                    return data
            return {}
        os.mkdir(cacheDir)
        return {}
    
    def write_cache(self, cache):
        cacheDir = os.path.join(os.getcwd(), 'cache')
        if os.path.isdir(cacheDir) == False:
            os.mkdir(cacheDir)
        with open(self.cacheFilePath, 'w+') as outfile:
            json.dump(cache, outfile)

    def spider_closed(self):
        self.write_cache(self.cache);

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(PostSpider, cls).from_crawler(crawler, *args, **kwargs)
        # crawler.signals.connect(spider.spider_opened, signals.spider_opened)
        return spider

    # def __init__(self, name=None, **kwargs):
    #     dispatcher.connect(self.spider_closed, signals.spider_closed)
    #     return super().__init__(name=name, **kwargs)