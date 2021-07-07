import requests
import json
from bs4 import BeautifulSoup

from ..meta_config import SPIDER_DATA_DIRNAME


def get_html(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""


def get_content(url):
    html = get_html(url)
    soup = BeautifulSoup(html, 'html.parser')
    paras_tmp = soup.select('.zw-title') + soup.select('p')
    paras = paras_tmp[0:]
    return paras


def generate_result(text, result):
    now = ''
    for t in text[:-2]:
        line = t.get_text().strip()
        if len(t) > 0:
            print(line)
            if line == '高风险地区：':
                now = '高风险地区'
            elif line == '中风险地区：':
                now = '中风险地区'
            elif now != '' and len(line.split()) != 0:
                result[now].append(line)


def risk_area_spider():
    url = 'http://www.gd.gov.cn/gdywdt/zwzt/yqfk/content/mpost_3021711.html'
    result = {'中风险地区': [], '高风险地区': []}
    text = get_content(url)
    generate_result(text, result)
    
    with open(f'{SPIDER_DATA_DIRNAME}/risk_areas.json', 'w+', encoding='utf-8') as f:
        f.write(json.dumps(result, ensure_ascii=False))


def main():
    risk_area_spider()


if __name__ == '__main__':
    main()
