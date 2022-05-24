# -*- coding: utf-8 -*-
import scrapy
import re
import requests
import os
import subprocess
import sys
from datetime import datetime

def write_to_log(str):
    file_name = "cospaco.log"
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cmd = f"echo '{date} {str}' >> {file_name}" 
    ret = subprocess.call(cmd, shell=True)
    if ret != 0:
        sys.exit(f'Exec cmd error: {cmd}, {ret}')

def getUrl(id, log):
    url = f'https://sukebei.nyaa.si/?f=0&c=2_2&q={id}'
    response = requests.get(url)
    selector = scrapy.Selector(text=response.text)

    table = selector.css('.table-responsive')

    if table:
        write_to_log(log + "\tTorrent exist: " + url)
    else:
        write_to_log(log + "\tTorrent Not Exist")


def parseSukebei(response):
    table = response.css('')
    if table is not None:
        print(table)

class CospacoSpider(scrapy.Spider):
    name = 'cospaco'

    page = 1

    allowed_domains = [
        'adult.contents.fc2.com',
    ]

    def start_requests(self):
        url = 'https://adult.contents.fc2.com/users/cospaco/'
        write_to_log("============================================================")
        yield scrapy.Request(url, self.parse)
    
    def parse(self, response):
        goods = response.css('.sell_block')
        for good in goods:
            if good is not None:
                img = good.css('.thum_img img::attr(src)').get()
                url = good.css('.info_block a::attr(href)').get()
                title = good.css('.info_block a::text').get()
                obj = re.match(r'^.*\?id=(\d+)$', url)
                if obj:
                    id = obj.group(1)
                    if id is not None:
                        log = f"{id}\t{title}\t{img}"
                        getUrl(id, log)
