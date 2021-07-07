import pandas

from meta_config import SPIDER_DATA_DIRNAME
from news.models import News


def news_importer():
    context = pandas.read_csv(f'{SPIDER_DATA_DIRNAME}/DXYNews-3.csv').loc[:, ['pubDate', 'title', 'summary', 'infoSource', 'sourceUrl']]
    for ind in range(10935):
        line = context.iloc[ind].values
        News.objects.get_or_create(title=line[1], defaults={
            'url': line[4],
            'media': line[3],
            'publish_time': line[0],
            'context': line[2]
        })


if __name__ == '__main__':
    news_importer()
