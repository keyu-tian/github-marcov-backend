import re
import json
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "marcov19.settings")
django.setup()
from risk.models import *
from country.models import City


def risk_area_storage():
    with open('./risk_areas.json', 'r+', encoding='utf-8') as f:
        data = json.loads(f.read())

    old_area = RiskArea.objects.all()
    while old_area.count():
        old_area.delete()
    for area in data['中风险地区']:
        section = re.split('[省市区]', area)
        province = section[0]
        city = section[1]
        res = City.objects.filter(name_ch=city)
        city = None if res is None else res.get()
        address = area
        level = 1
        kwargs = {'province': province, 'city': city, 'address': address, 'level': level}
        RiskArea.objects.create(**kwargs)
    for area in data['高风险地区']:
        section = re.split('[省市区]', area)
        province = section[0]
        city = section[1]
        res = City.objects.filter(name_ch=city)
        city = None if res is None else res.get()
        address = area
        level = 2
        kwargs = {'province': province, 'city': city, 'address': address, 'level': level}
        RiskArea.objects.create(**kwargs)


def main():
    risk_area_storage()


main()
