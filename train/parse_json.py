import argparse
import datetime
import json
import marcov19.settings
from django.conf import settings

settings.configure(DEBUG=True, default_settings=marcov19.settings)
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marcov19.settings')
import django

django.setup()

from country.models import Country, City
from train.models import Train, Station, MidStation
from utils.cast import address_to_jingwei


def parse_train_json(path):
    if not os.path.exists(path):
        os.makedirs(path)
    file = open(os.path.join(path, '火车班次json数据.json'), encoding='utf-8')
    while 1:
        result = file.readline()[: -1]
        if not result:
            break
        print(result)
        result = json.loads(result)
        print(result)
        country, flag = Country.objects.get_or_create(name_ch='中国', defaults={'name_en': 'Chinese'})
        name = list(result.get('trainInfo').keys())[0]
        if result:
            print('yes')
            dept_city_name = result.get('trainInfo').get(name).get('deptCity')
            dept_sta_name = result.get('trainInfo').get(name).get('deptStation')
            dept_time = result.get('trainInfo').get(name).get('deptTime')
            dept_date = result.get('trainInfo').get(name).get('deptTime')
            arri_city_name = result.get('trainInfo').get(name).get('deptCity')
            arri_sta_name = result.get('trainInfo').get(name).get('deptStation')
            arri_time = result.get('trainInfo').get(name).get('deptTime')
            arri_date = result.get('trainInfo').get(name).get('deptTime')

            dept_city, flag = City.objects.get_or_create(name_ch=dept_city_name)
            if flag:  # 数据库没有的新的国家，存名字
                dept_city.country = country
                dept_city.save()
            dept_sta, flag = Station.objects.get_or_create(name_cn=dept_sta_name)
            if flag:  # 数据库没有的新的火车站，存经纬度
                dept_sta.jingdu, dept_sta.weidu = address_to_jingwei(dept_sta_name + '站')
                dept_sta.city = dept_city
                dept_sta.save()

            arri_city, flag = City.objects.get_or_create(name_ch=arri_city_name)
            if flag:  # 数据库没有的新的国家，存名字
                arri_city.country = country
                arri_city.save()
            arri_sta, flag = Station.objects.get_or_create(name_cn=arri_sta_name)
            if flag:  # 数据库没有的新的火车站，存经纬度
                arri_sta.jingdu, arri_sta.weidu = address_to_jingwei(arri_sta_name + '站')
                arri_sta.city = arri_city
                arri_sta.save()
            train, flag = Train.objects.get_or_create(name=name, defaults={'dept_date': dept_date,
                                                                           'dept_time': dept_time,
                                                                           'arri_date': arri_date,
                                                                           'arri_time': arri_time})
            if flag:
                train.interval = result.get('extInfo').get('allTime')
                train.kilometer = result.get('extInfo').get('allMileage')
                mid_list = result.get('trainScheduleBody')
                for c in mid_list:
                    content = c.get('content')
                    sta, flag = Station.objects.get_or_create(name_cn=content[1])
                    if flag:  # 是新建，存经纬度
                        sta.jingdu, sta.weidu = address_to_jingwei(arri_sta_name + '站')
                        sta.city = arri_city
                        sta.save()
                    MidStation.objects.create(index=mid_list.index(c) + 1, arri_date=content[2],
                                              arri_time=content[3], station=sta, train=train)
            train.save()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Train-Spider')
    parser.add_argument('--path', required=False, default='train_crawler', type=str)
    args = parser.parse_args()

    start = str(datetime.datetime.now())
    print(f'[{start}] 开始parse...')
    parse_train_json(args.path)
    end = str(datetime.datetime.now())
    print('over')