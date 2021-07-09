import colorama


def misc_import():
    colorama.init(autoreset=True)
    from spiders.risk_importer import risk_import
    from spiders.news_importer import news_import
    from spiders.dxy_news_importer import dxy_news_import
    from spiders.yaoyan_importer import yaoyan_import
    from spiders.train_importer import train_import
    from spiders.travel_policy_importer import travel_policy_import

    print(colorama.Fore.CYAN + '[risk_import]:')
    risk_import()
    print(colorama.Fore.CYAN + '[news_import]:')
    news_import(delete_old_data=True)
    print(colorama.Fore.CYAN + '[dxy_news_import]:')
    dxy_news_import(delete_old_data=False)
    print(colorama.Fore.CYAN + '[yaoyan_import]:')
    yaoyan_import(line_start=0)
    print(colorama.Fore.CYAN + '[travel_policy_import]:')
    travel_policy_import(line_start=0)
    print(colorama.Fore.CYAN + '[train_import]:')
    train_import(line_start=0)
    

def epidemic_import():
    # todo
    ...
