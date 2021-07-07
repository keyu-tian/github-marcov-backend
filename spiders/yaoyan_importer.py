import argparse
import datetime
import json
import os

from tqdm import tqdm

from meta_config import IMPORTER_DATA_DIRNAME
from news.models import Rumor


def spider(path, line_start):
    with open(os.path.join(path, 'rumor.json'), 'r', encoding='utf-8') as file:
        bar = tqdm(list(enumerate(file.readlines())), dynamic_ncols=True)
    for line, result in bar:
        bar.set_description(f'[line{line}]')
        if line < line_start:
            continue
        try:
            result = json.loads(result)
        except:
            result = None
        if result:
            Rumor.objects.get_or_create(title=result['title'], defaults={
                'summary': result['summary'],
                'body': result['body'],
            })
        else:
            bar.set_postfix_str(f'failed!')


def yaoyan_import():
    parser = argparse.ArgumentParser(description='Train-Spider')
    parser.add_argument('--path', required=False, default=os.path.join(IMPORTER_DATA_DIRNAME, 'yaoyan_spider_all'), type=str)
    parser.add_argument('--line', required=False, default=0, type=int)
    args = parser.parse_args()
    start = str(datetime.datetime.now())
    print(f'[{start}] 开始parse...')
    spider(args.path, args.line)
    end = str(datetime.datetime.now())
    print('over')
