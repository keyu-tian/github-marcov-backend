import json
from tqdm import tqdm

from datetime import datetime

from meta_config import SPIDER_DATA_DIRNAME, BULK_CREATE_BATCH_SIZE
from news.models import News


def news_import(delete_old_data):
    if delete_old_data:
        News.objects.all().delete()
    
    with open(f'{SPIDER_DATA_DIRNAME}/news_data.json', 'r', encoding='utf-8') as f:
        data = json.loads(f.read())
        bar = tqdm(list(enumerate(data)), dynamic_ncols=True)
    
    objs = []
    for line, item in bar:
        bar.set_description(f'[line{line}]')
        bar.set_postfix_str(f'from {item["media_name"]}')
        kw = {
            'title': item['title'],
            'img': item['img'],
            'url': item['url'],
            'media': item['media_name'],
            'context': item['context'],
            'category_cn': item['category_cn'],
            'sub_category_cn': item['sub_category_cn'],
        }
        try:
            kw['publish_time'] = datetime.strptime(item['publish_time'][:10], '%Y-%m-%d').date()
        except:
            pass
        objs.append(News(**kw))
    bar.close()
    News.objects.bulk_create(objs, batch_size=BULK_CREATE_BATCH_SIZE)
