import json
import os

from selenium import webdriver
import argparse
from xml.dom.minidom import parse
import xml.dom.minidom
import requests

# 丁香医生辟谣爬取


def main(path):
    '''
    {
    "code": "success",
    "data": [
        {
            "body": "疫苗瓶的生产要求确实很高，按照国际标准，疫苗使用的容器必须为「一类中硼硅玻璃瓶」，如未达标，玻璃中析出的成份会影响疫苗药效，但是难度大不代表我们造不出来。在 2020 年疫情期间，中国建材已经无偿为疫苗研发机构提供了上千万个疫苗瓶。",
            "id": 196,
            "mainSummary": "2017 年前，我国还无法实现疫苗瓶的量产，但如今已成功突破这项技术瓶颈。",
            "rumorType": 0,
            "score": 210,
            "sourceUrl": "",
            "summary": "",
            "title": "中国企业造得出疫苗却造不出疫苗瓶？"
        },
        ]
    '''
    url = 'https://file1.dxycdn.com/2020/0130/454/3393874921745912507-115.json?t=27092733'
    response = requests.get(url, headers={'Content-Type': 'application/json'}, timeout=10)
    js = json.loads(response.text)
    if js['code'] == 'success':
        # with open('./spiders_data/rumor.json', 'a', encoding='utf-8') as fp:
        with open(os.path.join(path, 'rumor.json'), 'a', encoding='utf-8') as fp:
            for a in js['data']:
                fp.write(json.dumps({
                    'title': a['title'],
                    'summary': a['mainSummary'],
                    'body': a['body'],
                }) + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Train-Spider')
    parser.add_argument('--path', required=False, default=os.path.join('spiders_data', 'train_spider_all'), type=str)
    args = parser.parse_args()

    main(args.path)
