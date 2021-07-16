import json
import os
from datetime import datetime
# import marcov19.settings
# from django.conf import settings
#
# from utils.dict_ch import city_dict_ch
#
# settings.configure(DEBUG=True, default_settings=marcov19.settings)
# import os
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marcov19.settings')
# import django
#
# django.setup()

print("废了！！！！！！！！！！！！！！！！")
from tqdm import tqdm

from knowledge.models import EpidemicPolicy
from meta_config import SPIDER_DATA_DIRNAME, BULK_CREATE_BATCH_SIZE


def government_news_import(line_start=0):
    EpidemicPolicy.objects.all().delete()

    with open(os.path.join(SPIDER_DATA_DIRNAME, 'government_news.json'), 'r', encoding='utf-8') as file:
        bar = tqdm(list(enumerate(file.readlines())), dynamic_ncols=True)
    objs = []
    old_year = '2021-'
    last_month = 7
    for line, result in bar:
        bar.set_description(f'[line{line}]')
        if line < line_start:
            continue
        try:
            result = json.loads(result)
        except:
            result = None
        if result:
            this_month = int(result['date'].split('-')[0])
            if last_month == 1 and this_month == 12:
                old_year = '2020-'
            objs.append(EpidemicPolicy(
                title=result['title'],
                datetime=datetime.strptime(old_year + result['date'], "%Y-%m-%d %H:%M"),
                body=result['content'],
                src=result['src'],
            ))
            last_month = this_month
        else:
            bar.set_postfix_str(f'failed!')
    bar.close()
    EpidemicPolicy.objects.bulk_create(objs, batch_size=BULK_CREATE_BATCH_SIZE)


if __name__ == '__main__':
    government_news_import(0)
