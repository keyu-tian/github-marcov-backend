import base64
import json
import re
from datetime import datetime
from io import BytesIO

import requests
import math
from bs4 import BeautifulSoup
from django.views import View

from flight.models import Flight, Airport
from risk.views import get_city_risk_level
from utils.cast import address_to_jingwei
from utils.meta_wrapper import JSR


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
    fail_num = 0
    while True:
        if fail_num > 50:
            return '', '', '', '', '', ''
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')
        state = soup.find(attrs={'class': 'state'})
        if state is not None:
            city_num = len(state.find_all('div'))
            # print(city_num)
            condition = state.text.strip()[:2]
            city = soup.find_all('h2')
            dept_airport = re.split('[()]', city[0].text)[1].strip()
            arri_airport = re.split('[()]', city[-1].text)[1].strip()
            t = soup.find_all(attrs={'class': 'time'})
            dept_time = get_num_by_image(t[city_num].find('img').get('src'))
            arri_time = get_num_by_image(t[-1].find('img').get('src'))
            return code, condition, dept_airport, arri_airport, date + ' ' + dept_time + ':00', date + ' ' + arri_time + ':00'
        fail_num += 1


def get_flight_dept_and_arri_info_res(flight):
    # 传入flight对象，按交互文档travel/search格式返回dict
    risk = max(get_city_risk_level(flight.dept_airport.city_name), get_city_risk_level(flight.arri_airport.city_name))
    is_cancel = flight.condition == "取消"
    start = {
        'station_name': flight.dept_airport.airport_name,
        'city_name': flight.dept_airport.city_name,
        'country_name': flight.dept_airport.country_name,
        'risk': risk if not is_cancel else -1,
        'datetime': flight.dept_time
    }
    end = {
        'station_name': flight.arri_airport.airport_name,
        'city_name': flight.arri_airport.city_name,
        'country_name': flight.arri_airport.country_name,
        'risk': risk if not is_cancel else -1,
        'datetime': flight.arri_time
    }
    result = {
        'key': flight.code,
        'is_train': 0,
        'start': start,
        'end': end
    }
    return result


class TravelPlane(View):
    @JSR('status', 'stations', 'info', 'datetime')
    def post(self, request):
        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != {'number'}:
            return 1, [], {}, []
        code = kwargs['number']
        if Flight.objects.filter(code=code).count() == 0:
            return 2, [], {}, []
        flight = Flight.objects.filter(code=code).first()
        condition = flight.condition
        dept_airport = flight.dept_airport
        arri_airport = flight.arri_airport
        dept_time = flight.dept_time
        is_cancel = condition == "取消"
        start_station = {
            'station_name': dept_airport.airport_name,
            'city_name': dept_airport.city_name,
            'country_name': dept_airport.country_name,
            'risk_level': get_city_risk_level(dept_airport.city_name) if not is_cancel else -1,
            'pos': [dept_airport.jingdu, dept_airport.weidu]
        }
        end_station = {
            'station_name': arri_airport.airport_name,
            'city_name': arri_airport.city_name,
            'country_name': arri_airport.country_name,
            'risk_level': get_city_risk_level(arri_airport.city_name) if not is_cancel else -1,
            'pos': [arri_airport.jingdu, arri_airport.weidu]
        }
        stations = [start_station, end_station]
        risk_level = max(start_station['risk_level'], end_station['risk_level'])
        # if math.ceil(risk_level) >= 4:
        #     msg = '当前线路存在较大疫情风险，请谨慎考虑出行。'
        # elif math.ceil(risk_level) >= 1:
        #     msg = '当前线路存在疫情风险，请做好防护，谨慎出行。'
        # else:
        #     msg = '当前线路无疫情风险，请放心出行。'
        info = {
            'level': risk_level,
            'msg': '航班状态: ' + condition
        }
        return 0, stations, info, dept_time


class TravelCity(View):
    @JSR('status', 'planes')
    def post(self, request):
        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != {'start', 'end'}:
            return 1, []
        kwargs['start'] = kwargs['start'].split('市')[0]
        kwargs['end'] = kwargs['end'].split('市')[0]
        if Airport.objects.filter(city_name=kwargs['start']).count() != 0:
            flights = Flight.objects.filter(dept_airport__city_name=kwargs['start'], arri_airport__city_name=kwargs['end'])
        elif Airport.objects.filter(airport_name=kwargs['start']).count() != 0:
            flights = Flight.objects.filter(dept_airport__airport_name=kwargs['start'], arri_airport__airport_name=kwargs['end'])
        else:
            return 9, []
        plane_res = []
        for flight in flights:
            is_cancel = flight.condition == "取消"
            start = {'station_name': flight.dept_airport.airport_name,
                     'country_name': flight.dept_airport.country_name,
                     'city_name': flight.dept_airport.city_name,
                     'risk': get_city_risk_level(flight.dept_airport.city_name) if not is_cancel else -1,
                     'datetime': flight.dept_time}

            end = {'station_name': flight.arri_airport.airport_name,
                   'country_name': flight.arri_airport.country_name,
                   'city_name': flight.arri_airport.city_name,
                   'risk': get_city_risk_level(flight.arri_airport.city_name) if not is_cancel else -1,
                   'datetime': flight.arri_time}
            plane_res.append({'key': flight.code, 'start': start, 'end': end})

        return 0, plane_res
