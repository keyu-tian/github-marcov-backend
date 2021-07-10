import json
import os

# from django.conf import settings
#
# import marcov19.settings
#
# settings.configure(DEBUG=True, default_settings=marcov19.settings)
# import os
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marcov19.settings')
# import django
# django.setup()

from tqdm import tqdm

from country.models import Country, City, Province
from meta_config import SPIDER_DATA_DIRNAME, BULK_CREATE_BATCH_SIZE
from train.models import Train, Station, MidStation
from utils.cast import gd_address_to_jingwei_and_province_city
day_ch = ['第未知天', '第一天', '第二天', '第三天', '第四天', '第五天', '第六天', '第七天', '第八天', '第九天', '第十天', '终到站']


def cmp(a):
    a_content = a.get('content')
    if a_content[3] == '起点站':
        return '0'
    a_index = day_ch.index(a_content[2])
    return str(a_index) + a_content[3]


def train_import(line_start=0):
    MidStation.objects.all().delete()
    
    with open(os.path.join(SPIDER_DATA_DIRNAME, 'train_spider_all', '火车班次json数据.json'), 'r', encoding='utf-8') as file:
        bar = tqdm(list(enumerate(file.readlines())), dynamic_ncols=True)
    objs = []
    for line, result in bar:
        bar.set_description(f'[line{line}]')
        if line < line_start:
            continue
        try:
            result = json.loads(result)
        except:
            result = None
        if result:
            country, flag = Country.objects.get_or_create(name_ch='中国', defaults={'name_en': 'Chinese'})
            name = list(result.get('trainInfo').keys())[0]
            dept_city_name = result.get('trainInfo').get(name).get('deptCity')
            dept_sta_name = result.get('trainInfo').get(name).get('deptStation')
            dept_time = result.get('trainInfo').get(name).get('deptTime')
            dept_date = result.get('trainInfo').get(name).get('dptDate')
            arri_city_name = result.get('trainInfo').get(name).get('arriCity')
            arri_sta_name = result.get('trainInfo').get(name).get('arriStation')
            arri_time = result.get('trainInfo').get(name).get('arriTime')
            arri_date = result.get('trainInfo').get(name).get('arrDate')
            
            bar.set_postfix_str(f'{dept_city_name} => {arri_city_name}')
            
            dept_city, flag = City.objects.get_or_create(name_ch=dept_city_name)
            if flag:  # 数据库没有的新的city，存名字
                dept_city.country = country
                res = gd_address_to_jingwei_and_province_city(dept_city_name)
                if res is None:
                    dept_city.jingdu, dept_city.weidu = 0, 0
                    province_name = '未知'
                else:
                    dept_city.jingdu, dept_city.weidu = res['jingdu'], res['weidu']
                    province_name = res['province']
                dept_province, flag = Province.objects.get_or_create(name_ch=province_name)
                if flag:
                    dept_province.country = country
                    dept_province.save()
                dept_city.province = dept_province
                dept_city.save()
            dept_sta, flag = Station.objects.get_or_create(name_cn=dept_sta_name)
            if flag:  # 数据库没有的新的火车站，存经纬度
                res = gd_address_to_jingwei_and_province_city(dept_sta_name + '站')
                if res is None:
                    dept_sta.jingdu, dept_sta.weidu = 0, 0
                else:
                    dept_sta.jingdu, dept_sta.weidu = res['jingdu'], res['weidu']
                dept_sta.city = dept_city
                dept_sta.save()
            
            arri_city, flag = City.objects.get_or_create(name_ch=arri_city_name)
            if flag:  # 数据库没有的新的国家，存名字
                arri_city.country = country
                res = gd_address_to_jingwei_and_province_city(arri_city_name)
                if res is None:
                    arri_city.jingdu, arri_city.weidu = 0, 0
                    province_name = '未知'
                else:
                    arri_city.jingdu, arri_city.weidu = res['jingdu'], res['weidu']
                    province_name = res['province']
                arri_province, flag = Province.objects.get_or_create(name_ch=province_name)
                if flag:
                    arri_province.country = country
                    arri_province.save()
                arri_city.province = arri_province
                arri_city.save()
            arri_sta, flag = Station.objects.get_or_create(name_cn=arri_sta_name)
            if flag:  # 数据库没有的新的火车站，存经纬度
                res = gd_address_to_jingwei_and_province_city(arri_sta_name + '站')
                if res is None:
                    arri_sta.jingdu, arri_sta.weidu = 0, 0
                else:
                    arri_sta.jingdu, arri_sta.weidu = res['jingdu'], res['weidu']
                arri_sta.city = arri_city
                arri_sta.save()
            train, flag = Train.objects.get_or_create(name=name, defaults={'dept_date': dept_date,
                                                                           'dept_time': dept_time,
                                                                           'arri_date': arri_date,
                                                                           'arri_time': arri_time})
            if flag:
                train.dept_station = dept_sta
                train.arri_station = arri_sta
                train.dept_city = dept_city
                train.arri_city = arri_city
                train.interval = result.get('extInfo').get('allTime')
                train.kilometer = result.get('extInfo').get('allMileage')
                mid_list = result.get('trainScheduleBody')
                mid_list.sort(key=cmp)
                for c in mid_list:
                    content = c.get('content')
                    sta, flag = Station.objects.get_or_create(name_cn=content[1])
                    if flag:  # 是新建，存经纬度
                        res = gd_address_to_jingwei_and_province_city(content[1] + '站')
                        if res is None:
                            res = gd_address_to_jingwei_and_province_city(content[1])
                            if res is None:
                                continue
                        sta.jingdu, sta.weidu, city_name = res['jingdu'], res['weidu'], res['city']
                        mid_city, flag = City.objects.get_or_create(name_ch=city_name)
                        if flag:  # 数据库没有的新的国家，存名字
                            mid_city.country = country
                            res = gd_address_to_jingwei_and_province_city(city_name)
                            if res is None:
                                mid_city.jingdu, mid_city.weidu = 0, 0
                                province_name = '未知'
                            else:
                                mid_city.jingdu, mid_city.weidu = res['jingdu'], res['weidu']
                                province_name = res['province']
                            mid_province, flag = Province.objects.get_or_create(name_ch=province_name)
                            if flag:
                                mid_province.country = country
                                mid_province.save()
                            mid_city.province = mid_province
                            mid_city.save()
                        sta.city = mid_city
                        sta.save()
                    
                    objs.append(MidStation(
                        index=mid_list.index(c) + 1, arri_date=content[2],
                        arri_time=content[3], station=sta, train=train
                    ))
                train.save()
        else:
            bar.set_postfix_str(f'failed!')
    MidStation.objects.bulk_create(objs, batch_size=BULK_CREATE_BATCH_SIZE)

if __name__ == '__main__':
    train_import()