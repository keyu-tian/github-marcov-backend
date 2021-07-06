
import marcov19.settings
from django.conf import settings

settings.configure(DEBUG=True, default_settings=marcov19.settings)
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marcov19.settings')
import django

django.setup()
from django.views import View
from utils.meta_wrapper import JSR
import json
from flight.models import Flight
from utils.cast import address_to_jingwei
from risk.views import get_city_risk_level
from bs4 import BeautifulSoup
from selenium import webdriver
from django.db.models import Q
from country.models import Country, City


def get_flight_info_by_code(code):
    results = []
    flights = Flight.objects.filter(code__icontains=code)
    print(flights.count())
    if flights.count() == 0:
        return results
    for flight in flights:
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
    return results


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
    return None


def get_flight_dept_and_arri_info_res(flight):
    # 传入flight对象，按交互文档travel/search格式返回dict
    return {}


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
