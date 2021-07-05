import json
import os
import django
import sys
sys.path.extend(['C:\\Users\\wangzhen\\gitee-marcov-backend', 'D:\\Program Files\\JetBrains\\PyCharm 2020.2.3\\plugins\\python\\helpers\\pycharm', 'D:\\Program Files\\JetBrains\\PyCharm 2020.2.3\\plugins\\python\\helpers\\pydev'])
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "marcov19.settings")
django.setup()
from flight.models import *
from country.models import City


def news_storage():
    with open('./flights_data.json', 'r+', encoding='utf-8') as f:
        data = json.loads(f.read())

    # 如果想要在存新的新闻之前删去旧的，可以去掉下面三行的注释
    # old_news = News.objects.all()
    # while old_news.count():
    #     old_news.delete()
    total_code = []
    for line in data:
        # try:
        if line['code'] in total_code:
            continue
        total_code.append(line['code'])
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
    news_storage()


main()
