import argparse
import datetime
import json
import os

import requests
import sys
import time
import tqdm
from utils.log import create_logger
# 暂时不管Gxxx/Gxxx格式的版本
from requests.exceptions import Timeout

URL = 'http://train.qunar.com/qunar/checiInfo.jsp'
DEFAULT_DATE = datetime.datetime.now()
DEFAULT_DATE_STR = DEFAULT_DATE.strftime('%Y-%m-%d')  # 默认查询当天的

mingming = [('G', 9999),
            ('C', 9999),
            ('Z', 9999),
            ('T', 9999),
            ('K', 9999),
            ('L', 9999),
            ('Y', 999)]


def getinfo(logger, train_number='G99', date=DEFAULT_DATE_STR):
    logger.info('getinfo')
    params = {
        'method_name': 'buy',
        'ex_track': '',
        'q': train_number,
        'date': date.replace('-', ''),
        'format': 'json',
        'cityname': 123456,
        'ver': int(time.time() * 1000),
    }
    url = URL
    try:
        response = requests.get(url=url, params=params, headers={'Content-Type': 'application/json'}, timeout=10)
    except Timeout:
        logger.error('无法从服务器获取数据')
        logger.error('url: ' + url)
        logger.error(params)
        return None
    result = json.loads(response.text)
    if result == {'count': 0}:
        logger.error('无法获取该火车班次，班次为' + train_number)
        return None
    return result


def main(path, index=0, st=1):
    if not os.path.exists(path):
        os.makedirs(path)

    logger = create_logger(logger_name='spider', log_path=os.path.join(path, 'spider.log'), to_stdout=False)

    for a in range(index, len(mingming)):
        bar = tqdm.tqdm(range(st, mingming[a][1]))
        for i in bar:
            bar.set_description(f'[prefix={a}]')
            if 0 <= datetime.datetime.now().hour <= 6:
                time.sleep(0.5)
            else:
                time.sleep(1)
            name = mingming[a][0] + str(i)
            result = getinfo(logger=logger, train_number=name)  # result是json
            print(result)
            if result:
                with open(os.path.join(path, '火车班次json数据.json'), 'a', encoding='utf-8') as fp:
                    fp.write(json.dumps(result) + '\n')
                with open(os.path.join(path, '火车班次列表.json'), 'a', encoding='utf-8') as fp:
                    fp.write(name + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Train-Spider')
    parser.add_argument('--path', required=False, default='train_crawler', type=str)
    parser.add_argument('--index', required=False, default=0, type=int)
    parser.add_argument('--st', required=False, default=1, type=int)
    args = parser.parse_args()

    start = str(datetime.datetime.now())
    print(f'[{start}] 开始爬取，path={args.path}, index={args.index}, st={args.st}...')
    main(args.path, args.index, args.st)
    end = str(datetime.datetime.now())

    # res = getinfo('G1317')
    # print(res)

    # url = 'http://train.qunar.com/qunar/checiSuggest.jsp?callback=jQuery17208000492092391186_1460000280989&include_coach_suggest=true&lang=zh&q=G1316&sa=true&format=js&_=1460000429009'
    # try:
    #     response = requests.get(url=url, timeout=10)
    # except Timeout:
    #     logger.error('无法从服务器获取数据')
    #     logger.error('url: '+url)
    # results=json.loads('{'+response.text.split('({')[1].split('})')[0]+'}')['result']
    # print(results[0].get('key'))
