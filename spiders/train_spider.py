import argparse
import datetime
import json
import os
import time

import requests
from requests.exceptions import Timeout
from tqdm import tqdm

from meta_config import SPIDER_DATA_DIRNAME
from utils.cast import cur_time
from utils.logger import create_logger

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


def spider(verbose, path, index=0, st=1):
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
                    fp.write(f'index={current_index}, st={current_st + 1}\n')
                with open(os.path.join(path, '火车班次json数据.json'), 'a', encoding='utf-8') as fp:
                    fp.write(json.dumps(result) + '\n')
                with open(os.path.join(path, '火车班次列表.json'), 'a', encoding='utf-8') as fp:
                    fp.write(name + '\n')
            else:
                if verbose:
                    bar.set_description(f'[{name}]: failed')
                    bar.set_postfix_str('failed')


def main():
    """
    在单机上爬取
    """
    parser = argparse.ArgumentParser(description='Train-Spider')
    parser.add_argument('--verbose', required=False, default=True, type=bool)
    parser.add_argument('--path', required=False, default=os.path.join(SPIDER_DATA_DIRNAME, 'train_spider'), type=str)
    parser.add_argument('--index', required=False, default=0, type=int)
    parser.add_argument('--st', required=False, default=1, type=int)
    args = parser.parse_args()
    
    start = datetime.datetime.now().strftime('[%m-%d %H:%M:%S]')
    args.path += f'_index{args.index}_st{args.st}'
    print(f'{start} 开始爬！path={args.path}, index={args.index}, st={args.st}...')
    try:
        spider(args.verbose, args.path, args.index, args.st)
    except:
        with open(os.path.join(args.path, '火车班次爬到哪了.txt'), 'r', encoding='utf-8') as fp:
            s = fp.read()
            print(f'爬失败了，请你下次从 {s} 再开始爬！')
    else:
        print(f'爬完了！')


def distributed_main():
    """
    分布式爬取
    """
    print('请确保是tky在跑，否则请跑 main 而不是 distributed_main')
    from utils.pytorch_dist import TorchDistManager
    dist = TorchDistManager(cur_time(), 'auto', 'auto')
    path = os.path.join(SPIDER_DATA_DIRNAME, f'train_spider_distributed{dist.rank}')
    try:
        spider(dist.is_master(), path, dist.rank, 1)
    except:
        with open(os.path.join(path, '火车班次爬到哪了.txt'), 'r', encoding='utf-8') as fp:
            s = fp.read()
        print(f'[rk{dist.rank}] 爬失败了，请你下次从 {s.strip()} 再开始爬！')
    else:
        print(f'[rk{dist.rank}] 爬完了！')


if __name__ == '__main__':
    main()
