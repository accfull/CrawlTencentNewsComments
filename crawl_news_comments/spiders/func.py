# -*- coding: utf-8 -*-
import requests

headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
        }
def getHTMLText(url):
    try:
        r=requests.get(url, headers=headers)
        r.raise_for_status()
        r.encoding=r.apparent_encoding
        return r.text
    except:
        print("产生异常")

def ListCombiner(lst):
    string = ''
    for e in lst:
        string += e
    return string
