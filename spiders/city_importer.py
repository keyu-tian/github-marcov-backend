# coding:utf-8
from meta_config import IMPORTER_DATA_DIRNAME
import json
from country.models import City


def city_import():
    with open(f'{IMPORTER_DATA_DIRNAME}/code_to_city.json', 'r+', encoding='utf-8') as f:
        code_to_city = json.loads(f.read())
    for code, city in code_to_city.items():
        City.objects.get_or_create(name_ch=city, name_en='', code=code)

