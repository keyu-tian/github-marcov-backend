import argparse
import datetime
import json
import os
import re

from tqdm import tqdm

from country.models import Country, City
from meta_config import IMPORTER_DATA_DIRNAME
from train.models import Train, Station, MidStation
from utils.cast import address_to_jingwei, jingwei_to_address


def parse_train_json(path, line_start):
    with open(os.path.join(path, '火车班次json数据.json'), 'r', encoding='utf-8') as file:
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
                        sta.jingdu, sta.weidu = address_to_jingwei(content[1] + '站')
                        js = jingwei_to_address(sta.jingdu, sta.weidu)
                        city_name = re.findall(r'(.*)市', js['result']['addressComponent']['city'])
                        if len(city_name):
                            city_name = city_name[0]
                        else:
                            city_name = js['result']['addressComponent']['city']
                        mid_city, flag = City.objects.get_or_create(name_ch=city_name)
                        if flag:  # 数据库没有的新的国家，存名字
                            mid_city.country = country
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
    MidStation.objects.bulk_create(objs, batch_size=8192)


def train_import():
    parser = argparse.ArgumentParser(description='Train-Spider')
    parser.add_argument('--path', required=False, default=os.path.join(IMPORTER_DATA_DIRNAME, 'train_spider_all'), type=str)
    parser.add_argument('--line', required=False, default=0, type=int)
    args = parser.parse_args()
    start = str(datetime.datetime.now())
    print(f'[{start}] 开始parse...')
    parse_train_json(args.path, args.line)
    end = str(datetime.datetime.now())
    print('over')
