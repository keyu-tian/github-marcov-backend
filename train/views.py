import datetime
import json
import re
import time
import math

import requests
from django.db.models import Q
from django.views import View

from country.models import *
from flight.views import query_flight_info, get_flight_dept_and_arri_info_res
from risk.views import get_city_risk_level
from train.models import *
from requests import Timeout

from utils.cast import address_to_jingwei, jingwei_to_address
from utils.meta_wrapper import JSR

DEFAULT_DATE = datetime.datetime.now()
DEFAULT_DATE_STR = DEFAULT_DATE.strftime('%Y-%m-%d')

# 以get开头的返回json，以query开头的返回queryset或对象

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
    count = train.schedule_station.count() + 2
    total_risk_level += float(get_city_risk_level(train.dept_city)) / count
    for a in MidStation.objects.filter(train=train):
        risk_level = get_city_risk_level(a.station.city.name_ch)
        res['stations'].append({
            'station_name': a.station.name_cn,
            'city_name': a.station.city.name_ch,
            'risk_level': risk_level,
            'pos': [a.station.jingdu, a.station.weidu],
        })
        total_risk_level += float(risk_level) / count
    total_risk_level += float(get_city_risk_level(train.dept_city)) / count
    if math.ceil(total_risk_level) >= 4:
        msg = '当前线路存在较大疫情风险，请谨慎考虑出行。'
    elif math.ceil(total_risk_level) >= 1:
        msg = '当前线路存在疫情风险，请做好防护，谨慎出行。'
    else:
        msg = '当前线路无疫情风险，请放心出行。'
    res['info'] = {
        'level': math.ceil(total_risk_level) if math.ceil(total_risk_level) <= 5 else 5,
        'msg': msg,
    }
    return res


def get_train_dept_and_arri_info_res(train):
    res = {
    'start': {
        'city_name': train.dept_city.name_ch if train.dept_city else '未知',
        'country_name': train.dept_city.country if train.dept_city else '未知',
        'risk': get_city_risk_level(train.dept_city),
        'datetime': datetime.date.today().strftime("%Y-%m-%d ") + train.dept_time,
    },
    'end': {
        'city_name': train.arri_city.name_ch if train.arri_city else '未知',
        'country_name': train.arri_city.country if train.arri_city else '未知',
        'risk': get_city_risk_level(train.arri_city),
        'datetime': datetime.date.today().strftime("%Y-%m-%d ") + train.arri_time,
    },
    'key': train.name,
    'is_train': 0,
    }
    return res


def query_train_info(train_number):
    train = Train.objects.filter(name__icontains=train_number)
    if train.exists():
        return train
    else:
        result = search_train_by_number(train_number)
        country, flag = Country.objects.get_or_create(name_ch='中国', defaults={'name_en': 'Chinese'})
        if result and not Train.objects.filter(name=train_number).exists():
            dept_city_name = result.get('trainInfo').get(train_number).get('deptCity')
            dept_sta_name = result.get('trainInfo').get(train_number).get('deptStation')
            dept_time = result.get('trainInfo').get(train_number).get('deptTime')
            dept_date = result.get('trainInfo').get(train_number).get('dptDate')
            arri_city_name = result.get('trainInfo').get(train_number).get('arriCity')
            arri_sta_name = result.get('trainInfo').get(train_number).get('arriStation')
            arri_time = result.get('trainInfo').get(train_number).get('arriTime')
            arri_date = result.get('trainInfo').get(train_number).get('arrDate')
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
            return [train]
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
        if kwargs.keys() != {'number'}:
            return 1,
        try:
            key = kwargs['number']
        except:
            return -1,

        res = get_train_info_res(query_train_info(key)[0])
        if res:
            return 0, res['stations'], res['info']
        else:
            return 7,


class TravelSearch(View):
    @JSR('status', 'results')
    def post(self, request):
        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != {'key'}:
            return 1,
        try:
            key = kwargs['key']
        except:
            return -1,

        res = {'results': []}
        key_list = key.split(' ')
        for key in key_list:
            train_query = query_train_info(key)
            print(train_query)
            if train_query and not (len(train_query) == 1 and train_query[0] is None):
                for a in train_query:
                    res['results'].append(get_train_dept_and_arri_info_res(a))
            flight_query = query_flight_info(key)
            print(flight_query)
            if flight_query and not (len(flight_query) == 1 and flight_query[0] is None):
                for a in flight_query:
                    res['results'].append(get_flight_dept_and_arri_info_res(a))
        return 0, res


# class TravelPolicy(View):
#     @JSR('status', 'enter_policy', 'out_policy')
#     def post(self, request):
#         kwargs: dict = json.loads(request.body)
#         if kwargs.keys() != {'city'}:
#             return 1,
#         city_str = kwargs['city']
#         # 获取该地所属区
#         jingdu, weidu = address_to_jingwei(city_str)
#         city_name = jingwei_to_address(jingdu, weidu)['result']['addressComponent']['city']
#         # enter_policy = get_travel_enter_policy_msg(city_name)
#         # out_policy = get_travel_enter_policy_msg(city_name)
#         # if enter_policy == '':
#         #     # 获取省会
#         #     city_name = jingwei_to_address(jingdu, weidu)['result']['addressComponent']['province']
