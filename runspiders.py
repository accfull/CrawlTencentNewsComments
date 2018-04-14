# runspiders.py
import os
from crawl_news_comments.spiders.crawl_comments import crawlcomment
import json
os.system('scrapy crawl crawl_news')
comments_info_file='docs/comments_info.json'
f=open(comments_info_file)
line=f.readline()
# 从文件中读取评论页面链接，依次爬取
while line:
    info_dict=json.loads(line)
    print(info_dict['cmtId'],info_dict['newsId'])
    crawlcomment(info_dict['cmtId'],info_dict['date'],info_dict['newsId'])
    line = f.readline()
f.close()
