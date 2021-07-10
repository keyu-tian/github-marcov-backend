import json
import os

import requests
from tqdm import tqdm

# 丁香医生辟谣爬取
from meta_config import SPIDER_DATA_DIRNAME


def main():
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
    path = os.path.join(SPIDER_DATA_DIRNAME, 'yaoyan_spider_all')
    if not os.path.exists(path):
        os.makedirs(path)

    path = os.path.join(path, 'rumor.json')
    if os.path.exists(path):
        os.remove(path)
    
    url = 'https://file1.dxycdn.com/2020/0130/454/3393874921745912507-115.json?t=27092733'
    response = requests.get(url, headers={'Content-Type': 'application/json'}, timeout=10)
    js = json.loads(response.text)
    if js['code'] == 'success':
        # with open(f'{SPIDER_DATA_DIRNAME}/rumor.json', 'a', encoding='utf-8') as fp:
        with open(path, 'a', encoding='utf-8') as fp:
            bar = tqdm(list(enumerate(js['data'])))
            for line, a in bar:
                bar.set_description(f'[line{line}]')
                fp.write(json.dumps({
                    'title': a['title'],
                    'summary': a['mainSummary'],
                    'body': a['body'],
                }) + '\n')
            bar.close()


if __name__ == '__main__':
    main()
