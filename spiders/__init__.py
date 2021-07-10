import colorama


def re_import(name, launch_spider, *args, **kwargs):
    if launch_spider:
        print(colorama.Fore.CYAN + f'\n[{name}_spider]:')
        exec(f'from spiders.{name}_spider import main')
        exec(f'main()')
    print(colorama.Fore.CYAN + f'\n[{name}_importer]:')
    exec(f'from spiders.{name}_importer import {name}_import as main')
    exec(f'main(*args, **kwargs)')


def init_import(re_import_train):
    print(colorama.Fore.WHITE + '=> `init_import` started ...')
    
    from country.models import Country, City, Province
    colorama.init(autoreset=True)

    Country.objects.all().delete()
    City.objects.all().delete()
    Province.objects.all().delete()
    
    re_import('risk', True)
    re_import('news', True, delete_old_data=True)
    re_import('dxy_news', False, delete_old_data=False) # 不launch是因为 dxy_news 没有 spider，只有 importer
    re_import('yaoyan', True, line_start=0)
    re_import('travel_policy', True, line_start=0)
    if re_import_train:
        re_import('train', False, line_start=0)         # 不launch是因为 train 的 spider 太慢（超过6h）
    from spiders.station_exporter import station_export
    station_export()                            # 输出一个文件，给前端
    re_import('epidemic_domestic', False)               # 不launch是因为 epidemic_domestic 没有 spider，只有 importer
    re_import('epidemic_global', False)                 # 不launch是因为 epidemic_global 没有 spider，只有 importer
    re_import('flight_once', False)                     # 不launch是因为 flight_once 的 spider 太慢（超过2h），而且需要 chromedrive.exe

    print('')
    print(colorama.Fore.WHITE + '=> `init_import` finished.')
    
    daily_import()
    

def daily_import():
    print(colorama.Fore.WHITE + '=> `daily_import` started ...')
    
    re_import('flight_daily', False)
    # todo:
    # re_import('epidemic_domestic_daily', False)

    print('')
    print(colorama.Fore.WHITE + '=> `daily_import` finished.')
