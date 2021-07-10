# coding:utf-8
from meta_config import IMPORTER_DATA_DIRNAME
import json
from country.models import City, Country
from utils.cast import address_to_jingwei


def city_import():
    with open(f'{IMPORTER_DATA_DIRNAME}/code_to_city.json', 'r+', encoding='utf-8') as f:
        context = json.loads(f.read())
        code_to_city = context[0]
        city_to_country = context[1]
    for country in list(set(city_to_country.values())):
        Country.objects.get_or_create(name_ch=country)
    Country.objects.update_or_create(name_ch='中国')
    for code, city in code_to_city.items():
        jingdu, weidu = address_to_jingwei(city)
        City.objects.update_or_create(name_ch=city, name_en='', code=code, jingdu=jingdu, weidu=weidu, country=Country.objects.filter(name_ch=city_to_country.get(city, '中国')).get())

