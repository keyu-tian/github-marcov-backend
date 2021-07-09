def import_daily():
    # 王振，每天爬
    from spiders.risk_importer import risk_import
    # wlt，每天爬
    from spiders.news_importer import news_import
    # lrq，每天爬
    from spiders.epidemic_domestic_importer import epidemic_domestic_import
    # wcy，每天爬
    from spiders.epidemic_global_importer import epidemic_global_import
    
    # from spiders.flight_importer import flight_import

    import sys
    assert len(sys.argv) == 1
    sys.argv = sys.argv[1:]
    
    
    # for import_func in locals().values():
    #     import_func()
    
    exit(0)


def import_only_once():
    # wlt，爬一次
    from spiders.train_importer import train_import
    # wlt，爬一次
    from spiders.travel_policy_importer import travel_policy_import
    # wlt，爬一次
    from spiders.yaoyan_importer import yaoyan_import
    # 王振，爬一次
    from spiders.dxy_news_importer import dxy_news_import

    import sys
    assert len(sys.argv) == 1
    sys.argv = sys.argv[1:]
    # for import_func in locals().values():
    #     import_func()
    
    exit(0)
