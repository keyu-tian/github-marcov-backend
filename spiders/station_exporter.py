import json
import os

from meta_config import SPIDER_DATA_DIRNAME
from train.models import Station


def station_export():
    res = {}
    for a in Station.objects.all():
        if a.province_name + '.' + a.city_name in res.keys():
            res[a.province_name + '.' + a.city_name].append(a.name_ch)
        else:
            res[a.province_name + '.' + a.city_name] = [a.name_ch]
    province_json = {}
    for (key, value) in res.items():
        province = key.split('.')[0]
        city = key.split('.')[1]
        if province in province_json.keys():
            province_json[province].append({'city_name': city, 'stations_name': value})
        else:
            province_json[province] = [{'city_name': city, 'stations_name': value}]
    write_json = []
    for (key, value) in province_json.items():
        write_json.append({
            'provinceName': key,
            'cities': value,
        })
    with open(os.path.join(SPIDER_DATA_DIRNAME, 'stations.json'), 'w', encoding='utf-8') as fp:
        fp.write(json.dumps(write_json, indent=2, ensure_ascii=False))
