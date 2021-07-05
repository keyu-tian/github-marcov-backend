import datetime
import json
import re
import time
import math

import requests
from django.db.models import Q
from django.views import View

from country.models import *
from risk.views import get_city_risk_level
from train.models import *
from requests import Timeout

from utils.cast import address_to_jingwei, jingwei_to_address
from utils.meta_wrapper import JSR

DEFAULT_DATE = datetime.datetime.now()
DEFAULT_DATE_STR = DEFAULT_DATE.strftime('%Y-%m-%d')


def search_train_by_number(train_number='G99', date=DEFAULT_DATE_STR):
    # 返回值None为查询错误或不是列车号，不支持模糊匹配
    params = {
        'method_name': 'buy',
        'ex_track': '',
        'q': train_number,
        'date': date.replace('-', ''),
        'format': 'json',
        'cityname': 123456,
        'ver': int(time.time()*1000),
    }
    url = 'http://train.qunar.com/qunar/checiInfo.jsp'
    try:
        response = requests.get(url=url, params=params, headers={'Content-Type': 'application/json'}, timeout=10)
    except Timeout:
        return None
    result = json.loads(response.text)
    if result == {'count': 0}:
        return None
    return result


def get_train_info_res(train):
    res = {'stations': []}
    total_risk_level = 0
    count = train.schedule_station.count()
    for a in train.schedule_station.all():
        risk_level = get_city_risk_level(a.city.name_ch)
        res['stations'].append({
            'station_name': a.name_cn,
            'city_name': a.city.name_ch,
            'risk_level': risk_level,
            'pos': [a.jingdu, a.weidu],
        })
        total_risk_level += float(risk_level) / count
    res['info'] = {
        'level': math.ceil(total_risk_level) if math.ceil(total_risk_level) <= 5 else 5,
        'msg': '贴心话贴心话',  # todo：贴心话
    }
    return res


def query_train_info(train_number):
    train = Train.objects.filter(name=train_number)
    if train.exists():
        train = train.get()
        return get_train_info_res(train)
    else:
        result = search_train_by_number(train_number)
        country, flag = Country.objects.get_or_create(name_ch='中国', defaults={'name_en': 'Chinese'})
        if result and not Train.objects.filter(name=train_number).exists():
            dept_city_name = result.get('trainInfo').get(train_number).get('deptCity')
            dept_sta_name = result.get('trainInfo').get(train_number).get('deptStation')
            dept_time = result.get('trainInfo').get(train_number).get('deptTime')
            dept_date = result.get('trainInfo').get(train_number).get('deptTime')
            arri_city_name = result.get('trainInfo').get(train_number).get('deptCity')
            arri_sta_name = result.get('trainInfo').get(train_number).get('deptStation')
            arri_time = result.get('trainInfo').get(train_number).get('deptTime')
            arri_date = result.get('trainInfo').get(train_number).get('deptTime')
            dept_city, flag = City.objects.get_or_create(name_ch=dept_city_name)
            if flag:
                dept_city.country = country
                dept_city.save()
            dept_sta, flag = Station.objects.get_or_create(name_cn=dept_sta_name)
            if flag:  # 是新建，存经纬度
                dept_sta.jingdu, dept_sta.weidu = address_to_jingwei(dept_sta_name + '站')
                dept_sta.city = dept_city
                dept_sta.save()
            arri_city, flag = City.objects.get_or_create(name_ch=arri_city_name)
            if flag:
                arri_city.country = country
                arri_city.save()
            arri_sta, flag = Station.objects.get_or_create(name_cn=arri_sta_name)
            if flag:  # 是新建，存经纬度
                arri_sta.jingdu, arri_sta.weidu = address_to_jingwei(arri_sta_name + '站')
                arri_sta.city = arri_city
                arri_sta.save()
            train, flag = Train.objects.get_or_create(name=train_number, defaults={'dept_date': dept_date,
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
            return get_train_info_res(train)
    return None


def query_train_info_by_city(city_name):
    # return: query_set(Train)
    city = City.objects.filter(name_ch=city_name)
    if city.exists():
        city = city.get()
    else:
        jingdu, weidu = address_to_jingwei(city)
        js = jingwei_to_address(jingdu, weidu)
        city_name = re.findall(r'(.*)市', js['result']['addressComponent']['city'])
        if len(city_name):
            city_name = city_name[0]
        else:
            city_name = js['result']['addressComponent']['city']
        city = City.objects.filter(name_ch=city_name)
        if not city.exists():
            return None
        city = city.get()
    station_set = Station.objects.filter(city=city)
    train_set = Train.objects.filter(Q(schedule_station__city=city) | Q(dept_city=city) | Q(arri_city=city)).distinct()
    for a in station_set:
        query2 = a.start_train.all()
        query2 = (query2 | a.end_train.all()).distinct()
        train_set = (train_set | query2).distinct()
    return train_set


def get_train_info_by_city(city):
    # /travel/city接口，trains部分数据
    train_query_set = query_train_info_by_city(city)
    if train_query_set.count() == 0:
        return None
    res = {'trains': []}
    for a in train_query_set:
        ap = {'stations': [], 'number': a.name}
        mid_sta = a.schedule_station.all()
        for b in mid_sta:
            ap['stations'].append({
                'station_name': b.name_cn,
                'city_name': b.city.name_ch,
                'risk_level': 0,    # todo: 查询城市的风险等级
                'pos': [b.jingdu, b.weidu],
            })
        res['trains'].append(ap)
    return res


class TravelTrain(View):
    @JSR('status', 'stations', 'info')
    def post(self, request):
        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != {'rid', 'op'}:
            return 1,
        try:
            key = kwargs['number']
        except:
            return -1,

        res = query_train_info(key)
        if res:
            return 0, res['stations'], res['info']
        else:
            return 7,
