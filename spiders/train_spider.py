import argparse
import datetime
import json
import os

import requests
from tqdm import tqdm
import time
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
    # logger.info('getinfo')
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


def main(verbose, path, index=0, st=1):
    if not os.path.exists(path):
        os.makedirs(path)

    logger = create_logger(logger_name=os.path.basename(path), log_path=os.path.join(path, f'log.log'), to_stdout=False)

    for current_index in range(index, len(mingming)):
        if verbose:
            bar = tqdm(range(st, mingming[current_index][1]), dynamic_ncols=True)
        else:
            bar = range(st, mingming[current_index][1])
        for current_st in bar:
            if 0 <= datetime.datetime.now().hour <= 6:
                time.sleep(0.5)
            else:
                time.sleep(1)
            name = mingming[current_index][0] + str(current_st)
            result = getinfo(logger=logger, train_number=name)  # result是json
            # print(result)
            if result:
                data = list(result['trainInfo'].values())[0]
                if verbose:
                    bar.set_description(f'[{name}]')
                    bar.set_postfix_str(f'{data["deptCity"]} => {data["arriCity"]}')
                with open(os.path.join(path, '火车班次爬到哪了.txt'), 'w', encoding='utf-8') as fp:
                    fp.write(f'index={current_index}, st={current_st+1}')
                with open(os.path.join(path, '火车班次json数据.json'), 'a', encoding='utf-8') as fp:
                    fp.write(json.dumps(result) + '\n')
                with open(os.path.join(path, '火车班次列表.json'), 'a', encoding='utf-8') as fp:
                    fp.write(name + '\n')
            else:
                if verbose:
                    bar.set_description(f'[{name}]: failed')
                    bar.set_postfix_str('failed')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Train-Spider')
    parser.add_argument('--verbose', required=False, default=True, type=bool)
    parser.add_argument('--path', required=False, default=os.path.join('spiders_data', 'train_spider'), type=str)
    parser.add_argument('--index', required=False, default=0, type=int)
    parser.add_argument('--st', required=False, default=1, type=int)
    args = parser.parse_args()

    # [todo]@tky: 分布式爬取在这里写分布式的初始化，记得 verbose 设为 is_master

    start = datetime.datetime.now().strftime('[%m-%d %H:%M:%S]')
    args.path += f'_index{args.index}_st{args.st}'
    print(f'{start} 开始爬！path={args.path}, index={args.index}, st={args.st}...')
    try:
        main(args.verbose, args.path, args.index, args.st)
    except:
        with open(os.path.join(args.path, '火车班次爬到哪了.txt'), 'r', encoding='utf-8') as fp:
            s = fp.read()
            print(f'爬失败了，请你下次从 {s} 再开始爬！')
    print(f'爬完了！')

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
