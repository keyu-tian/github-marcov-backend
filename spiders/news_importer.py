import json

from meta_config import IMPORTER_DATA_DIRNAME
from news.models import News


def news_import():
    with open(f'{IMPORTER_DATA_DIRNAME}/news_data.json', 'r+', encoding='utf-8') as f:
        data = json.loads(f.read())
    
    # 如果想要在存新的新闻之前删去旧的，可以去掉下面三行的注释
    # old_news = News.objects.all()
    # while old_news.count():
    #     old_news.delete()
    for line in data:
        # try:
        News.objects.get_or_create(title=line['title'], defaults={
            'img': line['img'],
            'url': line['url'],
            'media': line['media_name'],
            'publish_time': line['publish_time'],
            'context': line['context'],
            'category_cn': line['category_cn'],
            'sub_category_cn': line['sub_category_cn'],
        })
        # except:
        #     print('插入新闻数据错误')
