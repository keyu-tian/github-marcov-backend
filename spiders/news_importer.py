import json
from tqdm import tqdm

from datetime import datetime

from meta_config import IMPORTER_DATA_DIRNAME
from news.models import News


def news_import(delete_old_data):
    if delete_old_data:
        News.objects.all().delete()
    
    with open(f'{IMPORTER_DATA_DIRNAME}/news_data.json', 'r+', encoding='utf-8') as f:
        data = json.loads(f.read())
        bar = tqdm(data, dynamic_ncols=True)
    
    for line in bar:
        bar.set_postfix_str(f'from {line["media_name"]}')
        defaults = {
            'img': line['img'],
            'url': line['url'],
            'media': line['media_name'],
            'context': line['context'],
            'category_cn': line['category_cn'],
            'sub_category_cn': line['sub_category_cn'],
        }
        try:
            defaults['publish_time'] = datetime.strptime(line['publish_time'][:10], '%Y-%m-%d').date()
        except:
            pass
        News.objects.get_or_create(title=line['title'], defaults=defaults)
