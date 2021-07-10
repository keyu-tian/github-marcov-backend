import json
import os
from meta_config import SPIDER_DATA_DIRNAME

# date -> str: 2021-07-09
def epidemic_China_total_import(date):
    China_data = {
        'new': {
            'died': 0,
            'cured': 0,
            'confirmed': 0,
        },
        'total': {
            'died': 0,
            'cured': 0,
            'confirmed': 0,
        },
    }
    provinces_json = os.path.join(SPIDER_DATA_DIRNAME, 'epidemic_domestic_data', 'province.json')
    provinces = json.load(open(provinces_json, 'r', encoding='utf-8'))
    data = None
    for it in provinces:
        if it['date'] == date:
            data = it
    if not data:
        print('日期不存在')
        return None
    for it in data['provinces']:
        China_data['total']['died'] += it['total']['died']
        China_data['total']['cured'] += it['total']['cured']
        China_data['total']['confirmed'] += it['total']['confirmed']
        China_data['new']['died'] += it['new']['died']
        China_data['new']['cured'] += it['new']['cured']
        China_data['new']['confirmed'] += it['new']['confirmed']

    return China_data

