# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs
import os

class CrawlNewsCommentsPipeline(object):
    def __init__(self):
        self.current_dir = os.getcwd()

    def process_item(self, item, spider):
        dir_path = self.current_dir + '/docs/' + item['source'] + '/' + item['date']

        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        news_file_path = dir_path + '/' + item['newsId'] + '.json'
        if os.path.exists(news_file_path) and os.path.isfile(news_file_path):
            print ('---------------------------------------')
            print (item['newsId'] + '.json exists, not overriden')
            print ('---------------------------------------')
            return item

        news_file = codecs.open(news_file_path, 'w', 'utf-8')
        line = json.dumps(dict(item),ensure_ascii=False)+'\n'
        news_file.write(line)
        news_file.close()

        #存储评论页信息
        comments_file_path=self.current_dir + '/docs/comments_info.json'
        comments_file=codecs.open(comments_file_path, 'a', 'utf-8')
        line1=json.dumps({'cmtId':item['cmtId'],'date':item['date'],'newsId':item['newsId']},ensure_ascii=False)+'\n'
        comments_file.write(line1)
        comments_file.close()

        return item
