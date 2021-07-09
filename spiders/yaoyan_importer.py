import json
import os

from tqdm import tqdm

from meta_config import IMPORTER_DATA_DIRNAME
from news.models import Rumor


def yaoyan_import(line_start=0):
    Rumor.objects.all().delete()
    
    with open(os.path.join(IMPORTER_DATA_DIRNAME, 'yaoyan_spider_all', 'rumor.json'), 'r', encoding='utf-8') as file:
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
