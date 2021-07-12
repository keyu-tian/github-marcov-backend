import os
import time

import requests
import json
from lxml import etree
from tqdm import tqdm

from meta_config import SPIDER_DATA_DIRNAME


import asyncio
from pyppeteer import launch


def government_news_wjw_spider():
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'h-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'sVoELocvxVW0S=58bPqwtYOlC3LEtoltijfLHcjm3Xj09Ze5lBkBMA0GyHEmXyTih.Q7o11RpcNw7FVvIiaTd4_K.s4Fpu7inMPLa; yfx_c_g_u_id_10006654=_ck21070514552219775935021607397; insert_cookie=97324480; enable_sVoELocvxVW0=true; yfx_f_l_v_t_10006654=f_t_1625468122966__r_t_1626111832117__v_t_1626111832117__r_c_2; security_session_verify=202bb7ffa580b87ed388b7e32cc47fd3; sVoELocvxVW0T=53iS5TKk7Iy9qqqm_bdQGsGg7GfTA8CVUdlA0rrYfZ4tTY8PLh43bs7WIKuyDw3kmxgZB63mujoRBCgTz.twEagXBz2g6TMqvDWt5Ih6FYtXDQXRTYVQa9Ztk448_dc6X41QoZp8AvzCTmqCC.UvqR5z1aSI5Q9QPdEaAdzQJWY9031Ys7Z9z7fDMsewOIybuxYdx6orHcw8K4KDqyotcbvPGQD81WnLLigCl_IIMIKg4RpNRXNG3EiK7dmus3mJC320NA4u_wUfDgIp17BkDDNxGPVS73ioy_PZsgrr0rto4GRZj3ivQSqQaVtG4Kxkf8LTy1u8szT4e2vQCWe0uQX',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.67'
    }
    with open(f'{SPIDER_DATA_DIRNAME}/government_news.json', 'r', encoding='utf-8') as f:
        bar = tqdm(list(enumerate(f)), dynamic_ncols=True)

    objs = []
    for line, result in bar:
        try:
            result = json.loads(result)
        except:
            result = None
        if result:
            res = requests.get(url=result['src'])
            tree = etree.HTML(res.content.decode("utf-8"))
            if len(tree.xpath('//*[@id="news-title"]')) == 0:
                continue
            save_json = {
                'date': result['date'],
                'content': result['content'],
                'title': tree.xpath('//*[@id="news-title"]')[0].text.strip(),
                'src': result['src'],
            }
            print(save_json)
            with open(os.path.join(SPIDER_DATA_DIRNAME, 'government_news_new.json'), 'a+', encoding='utf-8') as fp:
                fp.write(json.dumps(save_json) + '\n')


def main():
    government_news_wjw_spider()


if __name__ == '__main__':
    main()
