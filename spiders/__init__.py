import colorama


def re_import(name, launch_spider, *args, **kwargs):
    if launch_spider:
        print(colorama.Fore.CYAN + f'\n[{name}_spider]:')
        exec(f'from spiders.{name}_spider import main')
        exec(f'main()')
    print(colorama.Fore.CYAN + f'\n[{name}_importer]:')
    exec(f'from spiders.{name}_importer import {name}_import as main')
    exec(f'main(*args, **kwargs)')


def misc_delete_and_import():
    colorama.init(autoreset=True)

    re_import('risk', True)
    re_import('news', True, delete_old_data=True)
    re_import('dxy_news', False, delete_old_data=False) # 不launch是因为dxy_news没有爬虫，只有导入者
    re_import('yaoyan', True, line_start=0)
    re_import('travel_policy', True, line_start=0)
    re_import('train', False, line_start=0)

    print(colorama.Fore.GREEN + '=> finished.')
    

def epidemic_import():
    # todo
    ...
