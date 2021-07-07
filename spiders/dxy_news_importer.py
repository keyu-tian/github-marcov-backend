import pandas

from meta_config import IMPORTER_DATA_DIRNAME
from news.models import News


def dxy_news_import():
    context = pandas.read_csv(f'{IMPORTER_DATA_DIRNAME}/DXYNews-3.csv').loc[:, ['pubDate', 'title', 'summary', 'infoSource', 'sourceUrl']]
    for ind in range(10935):
        line = context.iloc[ind].values
        News.objects.get_or_create(title=line[1], defaults={
            'url': line[4],
            'media': line[3],
            'publish_time': line[0],
            'context': line[2]
        })
