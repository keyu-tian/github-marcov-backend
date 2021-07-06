import urllib.request
import json
import pandas
import marcov19.settings
from bs4 import BeautifulSoup

from django.conf import settings

settings.configure(DEBUG=True, default_settings=marcov19.settings)
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marcov19.settings')
import django

django.setup()
from news.models import *


def news_importer():
    context = pandas.read_csv('../spiders_data/DXYNews-3.csv').loc[:, ['pubDate', 'title', 'summary', 'infoSource', 'sourceUrl']]
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
