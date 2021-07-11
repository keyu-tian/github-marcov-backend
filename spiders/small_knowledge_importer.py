import json
import os
from knowledge.models import Knowledge
from meta_config import SPIDER_DATA_DIRNAME


def small_knowledge_importer():
    Knowledge.objects.all().delete()
    with open(os.path.join(SPIDER_DATA_DIRNAME, 'small_knowledge.json'), 'r', encoding='utf-8') as file:
        js = json.load(file)
    data = js['data']
    for a in data:
        Knowledge.objects.create(title=a['title'], body=a['body'])
