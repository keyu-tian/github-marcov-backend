from django.shortcuts import render
import json
from datetime import datetime, timedelta
from django.views import View
from django.db.models import Q
from news.models import *
from utils.meta_wrapper import JSR


class WeeklyNews(View):
    @JSR('status', 'date', 'china', 'global')
    def post(self, request):
        # new_news = news_spider()
        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != {'date'}:
            return 1, '', [], []
        res_china = []
        res_global = []
        # if News.objects.first().publish_time != new_news[0]['publish_time']:
        #     news_importer()
        if kwargs['date'] == '':
            end_date = datetime.now()
        else:
            try:
               end_date = datetime.strptime(kwargs['date'], '%Y-%m-%d')
            except:
                return 7, '', [], []
        for dis in range(7):
            now = end_date - timedelta(days=dis)
            now = now.strftime('%Y-%m-%d')
            query_china = News.objects.filter(sub_category_cn__iexact='国际社会', publish_time__icontains=now)
            query_global = News.objects.filter(sub_category_cn__icontains='国际社会', publish_time__icontains=now)
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
            query_china = News.objects.filter(~Q(media='BBC') & ~Q(media='CNN'), publish_time__icontains=now, img__isnull=True)
            # print(query_china)
            query_global = News.objects.filter(Q(media='BBC') | Q(media='CNN'), img__isnull=True, publish_time__icontains=now)
            oversea_keys = {'英格兰', '澳', '日本', '全美', '瑞士', '印尼', '智利', '老挝', '巴西', '印度', '新加坡', '泰', '首尔', '东京', '英国', '希腊', '美国'}
            for a in query_china:
                append, title = True, a.title
                for oversea_key in oversea_keys:
                    if oversea_key in title:
                        append = False
                        break
                if append:
                    res_china.append({
                        'title': a.title,
                        'body': a.context,
                        'url': a.url,
                        'publish_time': a.publish_time,
                        'media_name': a.media,
                        'img_url': '',
                    })
            for a in query_global:
                append, title = True, a.title
                for oversea_key in oversea_keys:
                    if oversea_key in title:
                        append = False
                        break
                if append:
                    res_global.append({
                        'title': a.title,
                        'body': a.context,
                        'url': a.url,
                        'publish_time': a.publish_time,
                        'media_name': a.media,
                        'img_url': '',
                    })
        return 0, end_date.strftime('%Y-%m-%d'), res_china, res_global

