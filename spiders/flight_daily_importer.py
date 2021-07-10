import datetime
import json

from country.models import City
from flight.models import Flight, Airport
from meta_config import IMPORTER_DATA_DIRNAME


def flight_daily_import():
    Flight.objects.all().delete()
    with open(f'{IMPORTER_DATA_DIRNAME}/flights_data.json', 'r+', encoding='utf-8') as f:
        data = json.loads(f.read())

    for line in data:
        dept_airport = line['dept_city']
        if Airport.objects.filter(airport_code=dept_airport).count() == 0:
            dept_airport = None
        else:
            dept_airport = Airport.objects.filter(airport_code=dept_airport).get()
        arri_airport = line['arri_city']
        if Airport.objects.filter(airport_code=arri_airport).count() == 0:
            arri_airport = None
        else:
            arri_airport = Airport.objects.filter(airport_code=arri_airport).get()
        if arri_airport is None or dept_airport is None:
            continue
        kwargs = {'code': line['code'], 'dept_time': line['dept_time'], 'dept_airport': dept_airport, 'arri_time': line['arri_time'], 'arri_airport': arri_airport, 'condition': line['condition']}
        Flight.objects.create(**kwargs)
        # except:
        #     print('插入新闻数据错误')
