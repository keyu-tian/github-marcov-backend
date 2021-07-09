import json
import os

from tqdm import tqdm

from country.models import Country, Policy, City, Province
from meta_config import IMPORTER_DATA_DIRNAME


def travel_policy_import(line_start=0):
    Policy.objects.all().delete()
    
    with open(os.path.join(IMPORTER_DATA_DIRNAME, 'travel_policy_spider_all', 'policy_by_city.json'), 'r', encoding='utf-8') as file:
        bar = tqdm(list(enumerate(file.readlines())), dynamic_ncols=True)
    country, created = Country.objects.get_or_create(name_ch='中国')
    for line, result in bar:
        bar.set_description(f'[line{line}]')
        if line < line_start:
            continue
        try:
            result = json.loads(result)
        except:
            result = None
        if result:
            policy, flag = Policy.objects.get_or_create(city_name=result['city'], defaults={
                'province_name': result['province'],
                'enter_policy': result['enter_policy'],
                'out_policy': result['out_policy'],
            })
            if flag:
                city, flag = City.objects.get_or_create(name_ch=result['city'])
                if flag:
                    city.country = country
                    city.save()
                policy.city = city
                province, flag = Province.objects.get_or_create(name_ch=result['province'])
                if flag:
                    province.country = country
                    province.save()
                policy.province = province
                policy.save()
        else:
            bar.set_postfix_str(f'failed!')
