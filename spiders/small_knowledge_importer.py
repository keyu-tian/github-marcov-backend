import json
import os
# import marcov19.settings
# from django.conf import settings
# settings.configure(DEBUG=True, default_settings=marcov19.settings)
# import os
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marcov19.settings')
# import django
# django.setup()
from knowledge.models import Knowledge
from meta_config import SPIDER_DATA_DIRNAME


def small_knowledge_importer():
    Knowledge.objects.all().delete()
    with open(os.path.join(SPIDER_DATA_DIRNAME, 'small_knowledge.json'), 'r', encoding='utf-8') as file:
        js = json.load(file)
    data = js['data']
    for a in data:
        Knowledge.objects.create(title=a['title'], body=a['body'], source=a['source'])


# if __name__ == '__main__':
#     small_knowledge_importer()