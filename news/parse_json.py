import re
import json
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "marcov19.settings")
django.setup()
from news.models import *


def news_storage():
    with open('./risk_areas.json', 'r+', encoding='utf-8') as f:
        data = json.loads(f.read())

    # 如果想要在存新的新闻之前删去旧的，可以去掉下面三行的注释
    # old_news = News.objects.all()
    # while old_news.count():
    #     old_news.delete()
    for line in data:
        try:
            kwargs = {'title': line['title'], 'img': line['img'], 'url': line['url'], 'media': line['media'], 'publish_time': line['publish_time'], 'context': line['context']}
            News.objects.create(**kwargs)
        except:
            print('插入新闻数据错误')


def main():
    news_storage()


main()
