import colorama

from meta_config import BULK_CREATE_BATCH_SIZE
from utils.cast import cur_time


def init_districts():
    print('\n' + colorama.Fore.WHITE + '=> `init_districts` started ...')
    
    from utils.country_dict import country_dict
    from utils.dict_ch import province_dict_ch
    from utils.locatable_cities import locatable_cities
    from country.models import Country, City, Province
    
    Country.objects.all().delete()
    Province.objects.all().delete()
    City.objects.all().delete()
    
    Country.objects.bulk_create([
        Country(name_ch=name_ch, name_en=name_en)
        for name_en, name_ch in country_dict.items()
    ], batch_size=BULK_CREATE_BATCH_SIZE)
    
    Province.objects.bulk_create([
        Province(
            name_ch=standard_province_name_ch,
            country=Country.get_via_name('中国'),
        )
        for standard_province_name_ch in set(province_dict_ch.values())
    ], batch_size=BULK_CREATE_BATCH_SIZE)

    # todo wz：在这里一次性导入全部国外城市和他们的经纬度。（似乎高德和百度都查不到国外城市！）
    kws = {}
    for _, (
        jingdu, weidu, district,
        standard_city_name_ch,
        not_standard_province_name_ch,
        not_standard_country_name_ch
    ) in locatable_cities.items():
        if standard_city_name_ch not in kws:
            kws[standard_city_name_ch] = dict(
                name_ch=standard_city_name_ch,
                jingdu=jingdu, weidu=weidu,
                province=Province.get_via_name(not_standard_province_name_ch),
                country=Country.get_via_name(not_standard_country_name_ch),
            )
    City.objects.bulk_create([
        City(**kw)
        for kw in kws.values()
    ], batch_size=BULK_CREATE_BATCH_SIZE)
    
    print('\n' + colorama.Fore.WHITE + '=> `init_districts` finished.')
    

def re_import(name, launch_spider, *args, **kwargs):
    if launch_spider:
        print(colorama.Fore.CYAN + f'\n[{cur_time()}][{name}_spider]:')
        exec(f'from spiders.{name}_spider import main')
        exec(f'main()')
    print(colorama.Fore.CYAN + f'\n[{cur_time()}][{name}_importer]:')
    exec(f'from spiders.{name}_importer import {name}_import as main')
    exec(f'main(*args, **kwargs)')


def init_import():
    colorama.init(autoreset=True)
    
    print('\n' + colorama.Fore.WHITE + '=> `init_import` started ...')
    
    init_districts()
    
    re_import('risk', True)
    re_import('news', True, delete_old_data=True)
    re_import('dxy_news', False, delete_old_data=False) # 不launch是因为 dxy_news 没有 spider，只有 importer
    re_import('yaoyan', True, line_start=0)
    re_import('travel_policy', True, line_start=0)
    re_import('train', False, line_start=0)         # 不launch是因为 train 的 spider 太慢（超过6h）
    from spiders.station_exporter import station_export
    station_export()                            # 输出一个文件，给前端
    re_import('epidemic_domestic', False)               # 不launch是因为 epidemic_domestic 没有 spider，只有 importer
    re_import('epidemic_global', False)                 # 不launch是因为 epidemic_global 没有 spider，只有 importer
    re_import('flight_once', False)                     # 不launch是因为 flight_once 的 spider 太慢（超过2h），而且需要 chromedrive.exe

    print('\n' + colorama.Fore.WHITE + '=> `init_import` finished.')
    
    daily_import()
    

def daily_import():
    print('\n' + colorama.Fore.WHITE + '=> `daily_import` started ...')
    
    re_import('flight_daily', False)
    # todo:
    # re_import('epidemic_domestic_daily', False)

    print('\n' + colorama.Fore.WHITE + '=> `daily_import` finished.')
