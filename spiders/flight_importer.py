import json
import marcov19.settings
import datetime
import argparse
from django.conf import settings

settings.configure(DEBUG=True, default_settings=marcov19.settings)
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marcov19.settings')
import django

django.setup()
from flight.models import *
from country.models import City


parser = argparse.ArgumentParser(description='Flight-Spider')
parser.add_argument('--date', required=False, type=str)
args = parser.parse_args()


def flights_storage(date):
    with open(f'../spiders_data/flights_data/flights_data{date}.json', 'r+', encoding='utf-8') as f:
        data = json.loads(f.read())

    for line in data:
        dept_city = line['dept_city']
        if City.objects.filter(code=dept_city).count() == 0:
            dept_city = None
        else:
            dept_city = City.objects.filter(code=dept_city).get()
        arri_city = line['arri_city']
        if City.objects.filter(code=arri_city).count() == 0:
            arri_city = None
        else:
            arri_city = City.objects.filter(code=arri_city).get()
        kwargs = {'code': line['code'], 'dept_time': line['dept_time'], 'dept_city': dept_city, 'arri_time': line['arri_time'], 'arri_city': arri_city, 'condition': line['condition']}
        Flight.objects.create(**kwargs)
        # except:
        #     print('插入新闻数据错误')


def main():
    if args.date:
        flights_storage(args.date)
    else:
        flights_storage(datetime.datetime.now().strftime('%Y-%m-%d'))


if __name__ == '__main__':
    main()
