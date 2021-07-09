import pandas
from tqdm import tqdm
from datetime import datetime

from meta_config import IMPORTER_DATA_DIRNAME
from news.models import News


def dxy_news_import(delete_old_data):
    if delete_old_data:
        News.objects.all().delete()
    
    target_keys = ['pubDate', 'title', 'summary', 'infoSource', 'sourceUrl']
    context: pandas.DataFrame = pandas.read_csv(f'{IMPORTER_DATA_DIRNAME}/DXYNews-3.csv').loc[:, target_keys]
    bar = tqdm(list(context.iterrows()), dynamic_ncols=True)
    
    for i, row in bar:
        bar.set_postfix_str(f'from {row["infoSource"]}')
        defaults = {
            'url': row['sourceUrl'],
            'media': row['infoSource'],
            'context': row['summary']
        }
        try:
            defaults['publish_time'] = datetime.strptime(row['pubDate'][:10], '%Y-%m-%d').date()
        except:
            pass
        News.objects.get_or_create(title=row['title'], defaults=defaults)
