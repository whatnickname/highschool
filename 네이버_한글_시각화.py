# -*- coding: utf-8 -*-
"""네이버 한글 시각화

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/14HbcF8vpMTzTyCna_nOHRxf3-9Qt5aAd
"""

import os
import sys
import urllib.request
import datetime
import time
import json

client_id = '0LHQM4VX_MQM6JfkXofa'
client_secret = 'OcPgqpswCg'

def getRequestUrl(url):
    req = urllib.request.Request(url)
    req.add_header("X-Naver-Client-Id", client_id)
    req.add_header("X-Naver-Client-Secret", client_secret)

    try:
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            print ("[%s] Url Request Success" % datetime.datetime.now())
            return response.read().decode('utf-8')
    except Exception as e:
        print(e)
        print("[%s] Error for URL : %s" % (datetime.datetime.now(), url))
        return None

def getPostData(post, jsonResult, cnt):
    title = post['title']
    description = post['description']
    org_link = post['originallink']
    link = post['link']

    pDate = datetime.datetime.strptime(post['pubDate'],  '%a, %d %b %Y %H:%M:%S +0900')
    pDate = pDate.strftime('%Y-%m-%d %H:%M:%S')

    jsonResult.append({'cnt':cnt, 'title':title, 'description': description,
'org_link':org_link,   'link': org_link,   'pDate':pDate})
    return

def getNaverSearch(node, srcText, start, display):
   base = "https://openapi.naver.com/v1/search"
   node = "/%s.json" % node
   parameters = "?query=%s&start=%s&display=%s" % (urllib.parse.quote(srcText), start,    display)
   url = base + node + parameters
   responseDecode = getRequestUrl(url)     #[CODE 1]
   if(responseDecode == None):
       return None
   else:
       return json.loads(responseDecode)

srcText='0'
def main():
    node = 'news'   # 크롤링 할 대상
    global srcText
    srcText = input('검색어를 입력하세요: ')
    cnt = 0
    jsonResult = []

    jsonResponse = getNaverSearch(node, srcText, 1, 100)  #[CODE 2]
    total = jsonResponse['total']

    while ((jsonResponse != None) and (jsonResponse['display'] != 0)):
        for post in jsonResponse['items']:
            cnt += 1
            getPostData(post, jsonResult, cnt)  #[CODE 3]

        start = jsonResponse['start'] + jsonResponse['display']
        jsonResponse = getNaverSearch(node, srcText, start, 100)  #[CODE 2]

    print('전체 검색 : %d 건' %total)

    with open('%s_naver_%s.json' % (srcText, node), 'w', encoding='utf8') as outfile:
        jsonFile = json.dumps(jsonResult,  indent=4, sort_keys=True,  ensure_ascii=False)

        outfile.write(jsonFile)

    print("가져온 데이터 : %d 건" %(cnt))
    print ('%s_naver_%s.json SAVED' % (srcText, node))

if __name__ == '__main__':
    main()

!pip install konlpy
!pip install Wordcloud

import json
import re
from konlpy.tag import Okt
from collections import Counter
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
from wordcloud import WordCloud

inputFileName = '%s_naver_news' % (srcText)
data = json.loads(open(inputFileName+'.json', 'r', encoding='utf-8').read())
data

message=''
for item in data:
    if 'description' in item.keys():
        message=message +re.sub(r'[^\w]','',item['description'])+''

nlp=Okt()
message_N=nlp.nouns(message)
message_N

count=Counter(message_N)
count

word_count=dict()
for tag, counts in count.most_common(80):
    if(len(str(tag))>1):
        word_count[tag] =counts
        print("%s : %d" % (tag,counts))

font_path="H2HDRM.TTF"
font_name=font_manager.FontProperties(fname=font_path).get_name()
matplotlib.rc('font',family=font_name)

plt.figure(figsize=(12,5))
plt.xlabel('키워드')
plt.ylabel('빈도수')
plt.grid(True)
sorted_Keys=sorted(word_count, key=word_count.get,reverse=True)
sorted_Values = sorted(word_count.values(), reverse=True)
plt.bar(range(len(word_count)), sorted_Values, align='center')
plt.xticks(range(len(word_count)), list(sorted_Keys), rotation=75)
plt.show()

wc = WordCloud(font_path, background_color='ivory', width=800, height=600)
cloud=wc.generate_from_frequencies(word_count)
plt.figure(figsize=(8,8))
plt.imshow(cloud)
plt.axis('off')
plt.show()