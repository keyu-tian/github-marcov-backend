from django.views import View
from utils.meta_wrapper import JSR
import json
import requests
from io import BytesIO
import base64
from flight.models import Flight
from utils.cast import address_to_jingwei
from risk.views import get_city_risk_level
from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import datetime
from django.db.models import Q
from country.models import Country, City


def get_num_by_image(url):
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=xVaNvyZ45BYWOSUAGqbYHkio&client_secret=MKZmvOt0t3Xr82u80WYpaGh2V2bKFmza'
    response = requests.get(host)
    access_token = response.json()['access_token']
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/numbers"
    # 二进制方式打开图片文件
    response = requests.get(url)
    # print(BytesIO(response.content).read())
    img = base64.b64encode(BytesIO(response.content).read())
    params = {"image": img}
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    res_time = response.json()['words_result'][0]['words']
    res_time = res_time[:2] + ':' + res_time[2:]
    return res_time


def get_flight_info_by_code(code, date=datetime.now().strftime('%Y-%m-%d')):
    url = f'http://www.umetrip.com/mskyweb/fs/fc.do?flightNo={code}&date={date}&channel='
    # print(res.text)
    fail_num = 0
    while True:
        if fail_num > 50:
            return '', '', '', '', '', ''
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')
        state = soup.find(attrs={'class': 'state'})
        if state is not None:
            condition = state.text.strip()
            city = soup.find(attrs={'title': code + ' 航班详情'})
            city = [x.strip() for x in city.text.split(' --- ')]
            dept_city = city[0]
            arri_city = city[1]
            t = soup.find_all(attrs={'class': 'time'})
            dept_time = get_num_by_image(t[1].find('img').get('src'))
            arri_time = get_num_by_image(t[2].find('img').get('src'))
            return code, condition, dept_city, arri_city, date + ' ' + dept_time + ':00', date + ' ' + arri_time + ':00'
        fail_num += 1


def get_flight_info_by_city(name, date):
    cities = City.objects.filter(name_ch=name)
    planes = []
    flights = []
    if cities.count() == 0:
        return []
    for city in cities:
        flights1 = city.start_flight.all()
        for flight in flights1:
            if flight.dept_time[:10] == date or flight.arri_time[:10] == date:
                flights.append(flight)
        flights2 = city.end_flight.all()
        for flight in flights2:
            if flight.dept_time[:10] == date or flight.arri_time[:10] == date:
                flights.append(flight)
    flights = list(set(flights))
    for flight in flights:
        start_city = flight.dept_city
        if start_city is None:
            start = {
                'country_name': '未知',
                'city_name': '未知',
                'risk_level': '未知',
                'pos': []
            }
        else:
            start = {'country_name': start_city.country.name_ch,
                     'city_name': start_city.name_ch,
                     'risk_level': get_city_risk_level(start_city.name_ch),
                     'pos': list(address_to_jingwei(start_city.name_ch))}
        end_city = flight.arri_city
        if end_city is None:
            end = {
                'country_name': '未知',
                'city_name': '未知',
                'risk_level': '未知',
                'pos': []
            }
        else:
            end = {'country_name': end_city.country.name_ch,
                   'city_name': end_city.name_ch,
                   'risk_level': get_city_risk_level(end_city.name_ch),
                   'pos': list(address_to_jingwei(end_city.name_ch))}
        planes.append({'number': flight.code, 'stations': [start, end]})
    return planes


def query_flight_info(flight_num):
    # 查询航班号，如果查询到，就直接返回Flight对象，如果没查到，就返回none
    flights = Flight.objects.filter(code__icontains=flight_num)
    if flights.count() == 0:
        return [None]
    result = []
    for flight in flights:
        result.append(flight)
    return result


def get_flight_dept_and_arri_info_res(flight):
    # 传入flight对象，按交互文档travel/search格式返回dict
    result = {'key': flight.code, 'is_train': 1}
    start = {}
    end = {}
    start_city = flight.dept_city
    end_city = flight.arri_city
    start['city_name'] = start_city.name_ch if start_city else '未知'
    start['country_name'] = start_city.country.name_ch if start_city and start_city.country else '未知'
    start['risk'] = address_to_jingwei(start['city_name']) if start_city else 0
    start['datetime'] = flight.dept_time
    end['city_name'] = end_city.name_ch if end_city else '未知'
    end['country_name'] = end_city.country.name_ch if end_city and end_city.country else '未知'
    end['risk'] = address_to_jingwei(end_city['city_name']) if end_city else 0
    end['datetime'] = flight.arri_time
    result['start'] = start
    result['end'] = end
    return result


class CountryFlightInfo(View):
    @JSR('status', 'planes')
    def post(self, request):
        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != {'name', 'date'}:
            return 1, []
        country = Country.objects.filter(name_ch=kwargs['name'])
        if country.count() == 0:
            return 6, []
        country = country.get()
        planes = []
        flights = []
        cities = country.country_city_set.all()
        for city in cities:
            flights1 = city.start_flight.all()
            for flight in flights1:
                if flight.dept_time[:10] == kwargs['date'] or flight.arri_time[:10] == kwargs['date']:
                    flights.append(flight)
            flights2 = city.end_flight.all()
            for flight in flights2:
                if flight.dept_time[:10] == kwargs['date'] or flight.arri_time[:10] == kwargs['date']:
                    flights.append(flight)
        flights = list(set(flights))
        for flight in flights:
            start_city = flight.dept_city
            if start_city is None:
                start = {
                    'country_name': '未知',
                    'city_name': '未知',
                    'risk_level': '未知',
                    'pos': []
                }
            else:
                start = {'country_name': start_city.country.name_ch,
                         'city_name': start_city.name_ch,
                         'risk_level': get_city_risk_level(start_city.name_ch),
                         'pos': list(address_to_jingwei(start_city.name_ch))}
            end_city = flight.arri_city
            if end_city is None:
                end = {
                    'country_name': '未知',
                    'city_name': '未知',
                    'risk_level': '未知',
                    'pos': []
                }
            else:
                end = {'country_name': end_city.country.name_ch,
                       'city_name': end_city.name_ch,
                       'risk_level': get_city_risk_level(end_city.name_ch),
                       'pos': list(address_to_jingwei(end_city.name_ch))}
            planes.append({'number': flight.code, 'stations': [start, end]})
        return 0, planes


class TravelPlane(View):
    @JSR('status', 'stations', 'info', 'datetime')
    def post(self, request):
        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != {'number'}:
            return 1, [], {}, []
        with open('flight/code_to_airport.json', 'r+', encoding='utf-8') as f:
            code_to_airport = json.loads(f.read())
        with open('flight/code_to_city.json', 'r+', encoding='utf-8') as f:
            code_to_city = json.loads(f.read())
        code, condition, dept_city, arri_city, dept_time, arri_time = get_flight_info_by_code(kwargs['number'])
        if code == '':
            return 1, [], {}, []
        stations = []
        try:
            arri_city = list(code_to_city.keys())[list(code_to_city.values()).index(arri_city)]
            dept_city = list(code_to_city.keys())[list(code_to_city.values()).index(dept_city)]
        except IndexError:
            print('你的城市表不全啊 giegie')
            return 1, [], {}, []
        print(code, condition, dept_city, arri_city, dept_time, arri_time)
        start_station = {
            'station_name': code_to_airport.get(dept_city, ''),
            'city_name': code_to_city.get(dept_city, ''),
        }
        if start_station['city_name']:
            start_station['risk_level'] = get_city_risk_level(start_station['city_name'])
            start_station['pos'] = list(address_to_jingwei(start_station['city_name']))
            city = City.objects.filter(name_ch__icontains=start_station['city_name'])
            print(city)
            if city.count() == 0:
                start_station['country_name'] = ''
            else:
                start_station['country_name'] = city.first().country.name_ch
        else:
            start_station['risk_level'] = 0
            start_station['pos'] = [0, 0]
            start_station['country_name'] = ''
        end_station = {
            'station_name': code_to_airport.get(arri_city, ''),
            'city_name': code_to_city.get(arri_city, ''),
        }
        if end_station['city_name']:
            end_station['risk_level'] = get_city_risk_level(end_station['city_name'])
            end_station['pos'] = list(address_to_jingwei(end_station['city_name']))
            city = City.objects.filter(name_ch__icontains=end_station['city_name'])
            if city.count() == 0:
                end_station['country_name'] = ''
            else:
                end_station['country_name'] = city.first().country.name_ch
        else:
            end_station['risk_level'] = 0
            end_station['pos'] = [0, 0]
            end_station['country_name'] = ''
        stations.append(start_station)
        stations.append(end_station)
        # msg = Policy.objects.filter(city_name=state_data.city_ch)
        # if msg.count() == 0:
        #     msg = '未知'
        # else:
        #     msg = msg.first().enter_policy+'\n'+msg.first().out_policy
        info = {
            'level': min(start_station['risk_level']+end_station['risk_level'], 5),
            'msg': '未知'
        }
        return 0, stations, info, dept_time
