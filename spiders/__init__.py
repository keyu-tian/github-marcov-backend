import colorama

from country.models import Country, City, Province


def re_import(name, launch_spider, *args, **kwargs):
    if launch_spider:
        print(colorama.Fore.CYAN + f'\n[{name}_spider]:')
        exec(f'from spiders.{name}_spider import main')
        exec(f'main()')
    print(colorama.Fore.CYAN + f'\n[{name}_importer]:')
    exec(f'from spiders.{name}_importer import {name}_import as main')
    exec(f'main(*args, **kwargs)')


def init_import(re_import_train):
    colorama.init(autoreset=True)

    Country.objects.all().delete()
    City.objects.all().delete()
    Province.objects.all().delete()
    
    re_import('risk', True)
    re_import('news', True, delete_old_data=True)
    re_import('dxy_news', False, delete_old_data=False) # 不launch是因为dxy_news没有爬虫，只有导入者
    re_import('yaoyan', True, line_start=0)
    re_import('travel_policy', True, line_start=0)
    if re_import_train:
        re_import('train', False, line_start=0)
    re_import('epidemic_domestic', False)
    re_import('flight_once', False)

    print('')
    print(colorama.Fore.WHITE + '=> finished.')
    

def daily_import():
    re_import('flight_daily', False)
    # todo:
    # re_import('epidemic_domestic_daily', False)

    print('')
    print(colorama.Fore.WHITE + '=> finished.')
