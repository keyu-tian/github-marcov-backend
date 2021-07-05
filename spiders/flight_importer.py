import json
import marcov19.settings
from django.conf import settings

settings.configure(DEBUG=True, default_settings=marcov19.settings)
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marcov19.settings')
import django

django.setup()
from flight.models import *
from country.models import City


def flights_storage():
    with open('./flights_data.json', 'r+', encoding='utf-8') as f:
        data = json.loads(f.read())

    # 如果想要在存新的新闻之前删去旧的，可以去掉下面三行的注释
    # old_news = News.objects.all()
    # while old_news.count():
    #     old_news.delete()
    for line in data:
        dept_city = line['dept_city']
        if City.objects.filter(code=dept_city).count() == 0:
            dept_city = None
        else:
            dept_city = City.objects.filter(code=dept_city).get()
        arri_city = line['arri_city']
        if City.objects.filter(code=dept_city).count() == 0:
            arri_city = None
        else:
            dept_city = City.objects.filter(code=dept_city).get()
        kwargs = {'code': line['code'], 'dept_time': line['dept_time'], 'dept_city': dept_city, 'arri_time': line['arri_time'], 'arri_city': arri_city, 'condition': line['condition']}
        Flight.objects.create(**kwargs)
        # except:
        #     print('插入新闻数据错误')


def main():
    flights_storage()


if __name__ == '__main__':
    main()
