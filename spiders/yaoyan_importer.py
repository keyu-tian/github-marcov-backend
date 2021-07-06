import argparse
import datetime
import json

from tqdm import tqdm

import marcov19.settings
from django.conf import settings

settings.configure(DEBUG=True, default_settings=marcov19.settings)
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marcov19.settings')
import django

django.setup()

from news.models import *


def main(path, line_start):
    # with open('./spiders_data/rumor.json', 'r', encoding='utf-8') as file:
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


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Train-Spider')
    parser.add_argument('--path', required=False, default=os.path.join('spiders_data', 'train_spider_all'), type=str)
    parser.add_argument('--line', required=False, default=0, type=int)
    args = parser.parse_args()

    start = str(datetime.datetime.now())
    print(f'[{start}] 开始parse...')
    main(args.path, args.line)
    end = str(datetime.datetime.now())
    print('over')