# @tky，跑完train_importer后跑这个，导出station_list给前端
# 需要import django的设置
import json
import marcov19.settings
from django.conf import settings

from utils.dict_ch import city_dict_ch

settings.configure(DEBUG=True, default_settings=marcov19.settings)
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marcov19.settings')
import django
django.setup()
from train.models import Station


def station_exporter():
    res = {}
    for a in Station.objects.all():
        if a.city and a.city.province and a.city.province.name_ch + '.' + a.city.name_ch in res.keys():
            res[a.city.province.name_ch + '.' + a.city.name_ch].append(a.name_cn)
        else:
            res[a.city.province.name_ch + '.' + a.city.name_ch] = [a.name_cn]
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
    with open('stations.json', 'w+', encoding='utf-8') as fp:
        fp.write(json.dumps(write_json))


if __name__ == '__main__':
    station_exporter()