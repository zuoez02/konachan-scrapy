# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.pipelines.images import FilesPipeline
from scrapy.exceptions import DropItem
import logging


class PostFilePipeline(FilesPipeline):
    def file_path(self, request, response=None, info=None):
        original_path = super(PostFilePipeline, self).file_path(request, response=None, info=None)
        sha1_and_extension = original_path.split('/')[1] # delete 'full/' from the path
        filename = request.meta.get('filename', '') + "_" + sha1_and_extension
        folder = request.meta.get('folder', '')
        return folder + '/' + filename

    def get_media_requests(self, item, info):
        file_urls = item['file_urls'][0]
        meta = {'filename': item['id'], 'folder': item['folder']}
        for file_url in item['file_urls']:
            yield scrapy.Request(url=file_url, meta=meta)

    def item_completed(self, results, item, info):
        file_urls = [x['path'] for ok, x in results if ok]
        if not file_urls:
            raise DropItem("Item contains no files")
        item['file_urls'] = file_urls
        return item