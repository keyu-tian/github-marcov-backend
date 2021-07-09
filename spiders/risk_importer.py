import json
import re

from tqdm import tqdm

from meta_config import IMPORTER_DATA_DIRNAME
from risk.models import RiskArea
from utils.cast import address_to_jingwei


def risk_import():
    RiskArea.objects.all().delete()
    
    with open(f'{IMPORTER_DATA_DIRNAME}/risk_areas.json', 'r+', encoding='utf-8') as f:
        data = json.loads(f.read())
    
    for level_num, level_str in ((1, '中'), (2, '高')):
        bar = tqdm(data[level_str + '风险地区'], dynamic_ncols=True)
        for area in bar:
            bar.set_description(level_str + '风险：')
            section = re.split('[省市区]', area)
            province = section[0]
            city = section[1]
            address = area
            jingdu, weidu = address_to_jingwei(address)
            bar.set_postfix(地址=area, 经度=jingdu, 纬度=weidu)
            kwargs = {'province': province, 'city': city, 'address': address, 'level': level_num, 'jingdu': jingdu, 'weidu': weidu}
            RiskArea.objects.create(**kwargs)
