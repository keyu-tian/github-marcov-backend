import json
import os

from tqdm import tqdm

from country.models import Policy
from meta_config import SPIDER_DATA_DIRNAME


def travel_policy_import(line_start=0):
    Policy.objects.all().delete()
    
    with open(os.path.join(SPIDER_DATA_DIRNAME, 'travel_policy_spider_all', 'policy_by_city.json'), 'r', encoding='utf-8') as file:
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
            Policy.objects.get_or_create(
                city_name=result['city'], defaults=dict(
                    province_name=result['province'],
                    enter_policy=result['enter_policy'],
                    out_policy=result['out_policy'],
                )
            )
        else:
            bar.set_postfix_str(f'failed!')
