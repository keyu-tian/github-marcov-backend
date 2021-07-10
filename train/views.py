import datetime
import json
import math

from django.views import View

from flight.views import query_flight_info, get_flight_dept_and_arri_info_res
from risk.views import get_city_risk_level
from train.models import Train, MidStation
from utils.meta_wrapper import JSR

DEFAULT_DATE = datetime.datetime.now()
DEFAULT_DATE_STR = DEFAULT_DATE.strftime('%Y-%m-%d')


def get_train_info_res(train: Train):
    res = {'stations': []}
    total_risk_level = 0
    count = train.schedule_station.count() + 2
    total_risk_level += float(get_city_risk_level(train.dept_city)) / count
    for a in MidStation.objects.filter(train=train):
        risk_level = get_city_risk_level(a.station.city.name_ch)
        res['stations'].append({
            'station_name': a.station.name_ch,
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


def get_train_dept_and_arri_info_res(train: Train):
    hours, minutes = map(int, train.interval.strip('分钟').split('小时'))
    st_t = datetime.datetime.strptime(datetime.date.today().strftime('%Y-%m-%d ') + train.dept_time, '%Y-%m-%d %H:%M')
    ed_t = st_t + datetime.timedelta(hours=hours, minutes=minutes)
    res = {
        'start': {
            'station_name': train.dept_station.name_ch,
            'city_name': train.dept_city.name_ch,
            'country_name': train.dept_city.country.name_ch,
            'risk': get_city_risk_level(train.dept_city),
            'datetime': st_t.strftime('%Y-%m-%d %H:%M'),
        },
        'end': {
            'station_name': train.arri_station.name_ch,
            'city_name': train.arri_city.name_ch,
            'country_name': train.arri_city.country.name_ch,
            'risk': get_city_risk_level(train.arri_city),
            'datetime': ed_t.strftime('%Y-%m-%d %H:%M'),
        },
        'key': train.name,
        'is_train': 1,
    }
    return res


# def query_train_info_by_city(query_name):
#     # return: query_set(Train)
#     city = City.objects.filter(name_ch=query_name)
#     if city.exists():
#         city = city.get()
#     else:
#         city_name = gd_address_to_jingwei_and_province_city(query_name)['city']
#         city = City.objects.filter(name_ch=city_name)
#         if not city.exists():
#             return None
#         city = city.get()
#     station_set = Station.objects.filter(city=city)
#     train_set = Train.objects.filter(Q(schedule_station__city=city) | Q(dept_city=city) | Q(arri_city=city)).distinct()
#     for a in station_set:
#         query2 = a.start_train.all()
#         query2 = (query2 | a.end_train.all()).distinct()
#         train_set = (train_set | query2).distinct()
#     return train_set
#
#
# def get_train_info_by_city(city):
#     # /travel/city接口，trains部分数据
#     train_query_set = query_train_info_by_city(city)
#     if train_query_set.count() == 0:
#         return None
#     res = {'trains': []}
#     for a in train_query_set:
#         ap = {'stations': [], 'number': a.name}
#         mid_sta = a.schedule_station.all()
#         for b in mid_sta:
#             ap['stations'].append({
#                 'station_name': b.name_ch,
#                 'city_name': b.city.name_ch,
#                 'risk_level': 0,  # todo: 查询城市的风险等级
#                 'pos': [b.jingdu, b.weidu],
#             })
#         res['trains'].append(ap)
#     return res


class TravelTrain(View):
    @JSR('status', 'stations', 'info')
    def post(self, request):
        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != {'number'}:
            return 1
        key = kwargs['number'].upper()
        
        train = Train.objects.filter(name=key)
        if train.count() == 0:
            return 7
        res = get_train_info_res(train.get())
        return 0, res['stations'], res['info']


class TravelSearch(View):
    @JSR('status', 'results')
    def post(self, request):
        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != {'key'}:
            return 1
        key = kwargs['key'].upper()
        
        if len(key) < 3 and key not in {
            'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8',
            'Z1', 'Z2', 'Z3', 'Z4', 'Z5', 'Z6', 'Z7', 'Z8', 'Z9',
            'T1', 'T2', 'T9',
            'K3', 'K5', 'K6'
        }:
            return 3
        
        res = []
        for key in key.split(' '):
            for a in Train.objects.filter(name__icontains=key):
                res.append(get_train_dept_and_arri_info_res(a))
            for a in query_flight_info(key):
                res.append(get_flight_dept_and_arri_info_res(a))
        return 0, {'results': res}


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
