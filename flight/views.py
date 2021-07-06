
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
    # options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    # options.add_argument(
    #     f'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
    # driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=options)

    # url = f'http://www.umetrip.com/mskyweb/fs/fa.do?dep={src}&arr={dst}&date={args.date if args.date else now}&channel='  # time:2021-07-02
    # driver.get(url)
    # fail_num = 0
    # while True:
    #     elem = driver.find_element_by_xpath("//*")
    #     source_code = elem.get_attribute("outerHTML")
    #     soup = BeautifulSoup(source_code, 'html.parser')
    #     flights = soup.find_all(attrs={'class': 'li_com'})
    #     err = soup.find_all(attrs={'class': 'err_com'})
    #     if len(err) > 0:
    #         fail_num += 1
    #         if fail_num > 5:
    #             break
    #         driver.refresh()
    #         continue
    #     fail_num = 0
    #     for flight in flights:
    #         context = flight.get_text().strip().split()
    #         # print(context)
    #         results.append({'code': context[0][:-4], 'dept_time': now + ' ' + (context[1] if context[2] == "--" else context[2]) + ':00', 'arri_time': now + ' ' + (context[4] if context[5] == "--" else context[5]) + ':00', 'condition': context[6], 'dept_city': src, 'arri_city': dst})
    #     try:
    #         next_page = driver.find_element_by_css_selector('#p_next')
    #         next_page.click()
    #     except:
    #         break

    # driver.quit()


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


# Create your views here.
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


if __name__ == '__main__':
    ret = get_flight_info_by_code('N')
    print(ret)