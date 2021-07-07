import argparse
import datetime
import json
import os

from tqdm import tqdm

from country.models import Country, Policy, City, Province
from meta_config import IMPORTER_DATA_DIRNAME


def spider(path, line_start):
    with open(os.path.join(path, 'policy_by_city.json'), 'r', encoding='utf-8') as file:
        bar = tqdm(list(enumerate(file.readlines())), dynamic_ncols=True)
    country = Country.objects.get(name_ch='中国')
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


def travel_policy_import():
    parser = argparse.ArgumentParser(description='Train-Spider')
    parser.add_argument('--path', required=False, default=os.path.join(IMPORTER_DATA_DIRNAME, 'travel_policy_spider_all'), type=str)
    parser.add_argument('--line', required=False, default=0, type=int)
    args = parser.parse_args()
    start = str(datetime.datetime.now())
    print(f'[{start}] 开始parse...')
    spider(args.path, args.line)
    print('over')
