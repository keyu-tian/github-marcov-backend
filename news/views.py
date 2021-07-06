from django.shortcuts import render
from django.views import View
from news.models import *
from utils.meta_wrapper import JSR
from spiders.news_spider import news_spider
from spiders.news_importer import news_importer


class WeeklyNews(View):
    @JSR('status', 'china', 'global')
    def post(self, request):
        new_news = news_spider()
        res_china = []
        res_global = []
        if News.objects.first().publish_time != new_news[0].publish_time:
            news_importer()
        query_china = News.objects.filter(sub_category_cn__iexact='国际社会')
        query_global = News.objects.filter(sub_category_cn__icontains='国际社会')
        for a in query_china:
            res_china.append({
                'title': a.title,
                'body': a.context,
                'url': a.url,
                'publish_time': a.publish_time,
                'media_name': a.media,
                'img_url': a.img,
            })
        for a in query_global:
            res_global.append({
                'title': a.title,
                'body': a.context,
                'url': a.url,
                'publish_time': a.publish_time,
                'media_name': a.media,
                'img_url': a.img,
            })
        return 0, res_china, res_global

