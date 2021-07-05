import re
import json
import os
import django
import sys
sys.path.extend(['C:\\Users\\wangzhen\\gitee-marcov-backend', 'D:\\Program Files\\JetBrains\\PyCharm 2020.2.3\\plugins\\python\\helpers\\pycharm', 'D:\\Program Files\\JetBrains\\PyCharm 2020.2.3\\plugins\\python\\helpers\\pydev'])
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "marcov19.settings")
django.setup()
from risk.models import *
from utils.cast import address_to_jingwei


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
        address = area
        jingdu, weidu = address_to_jingwei(address)
        print(jingdu, weidu)
        level = 1
        kwargs = {'province': province, 'city': city, 'address': address, 'level': level, 'jingdu': jingdu, 'weidu': weidu}
        RiskArea.objects.create(**kwargs)
    for area in data['高风险地区']:
        section = re.split('[省市区]', area)
        province = section[0]
        city = section[1]
        address = area
        level = 2
        kwargs = {'province': province, 'city': city, 'address': address, 'level': level}
        RiskArea.objects.create(**kwargs)


def main():
    risk_area_storage()


main()
