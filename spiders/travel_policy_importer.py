import json
import os

from tqdm import tqdm

from country.models import Country, Policy, City, Province
from meta_config import SPIDER_DATA_DIRNAME


def travel_policy_import(line_start=0):
    Policy.objects.all().delete()
    
    with open(os.path.join(SPIDER_DATA_DIRNAME, 'travel_policy_spider_all', 'policy_by_city.json'), 'r', encoding='utf-8') as file:
        bar = tqdm(list(enumerate(file.readlines())), dynamic_ncols=True)
    # todo wlt：删除这里；因为国家是一次性导入的，在这里不要再用get_or_create
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
                # todo wlt：删除这里；因为城市是一次性导入的，在这里不要再用get_or_create
                city, flag = City.objects.get_or_create(name_ch=result['city'])
                if flag:
                    city.country = country
                    city.save()
                policy.city = city
                # todo wlt：删除这里；因为省是一次性导入的，在这里不要再用get_or_create
                province, flag = Province.objects.get_or_create(name_ch=result['province'])
                if flag:
                    province.country = country
                    province.save()
                policy.province = province
                policy.save()
        else:
            bar.set_postfix_str(f'failed!')
