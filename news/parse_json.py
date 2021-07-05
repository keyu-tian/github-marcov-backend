import json
import os
import django
import sys
sys.path.extend(['C:\\Users\\wangzhen\\gitee-marcov-backend', 'D:\\Program Files\\JetBrains\\PyCharm 2020.2.3\\plugins\\python\\helpers\\pycharm', 'D:\\Program Files\\JetBrains\\PyCharm 2020.2.3\\plugins\\python\\helpers\\pydev'])
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "marcov19.settings")
django.setup()
from news.models import *


def news_storage():
    with open('./news.json', 'r+', encoding='utf-8') as f:
        data = json.loads(f.read())

    # 如果想要在存新的新闻之前删去旧的，可以去掉下面三行的注释
    # old_news = News.objects.all()
    # while old_news.count():
    #     old_news.delete()
    for line in data:
        # try:
        kwargs = {'title': line['title'], 'img': line['img'], 'url': line['url'], 'media': line['media_name'], 'publish_time': line['publish_time'], 'context': line['context']}
        News.objects.create(**kwargs)
        # except:
        #     print('插入新闻数据错误')


def main():
    news_storage()


main()
