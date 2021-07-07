from django.shortcuts import render
import json
from datetime import datetime, timedelta
from django.views import View
from django.db.models import Q
from news.models import *
from utils.meta_wrapper import JSR


class WeeklyNews(View):
    OVERSEA_KEYS = {'英格兰', '澳', '日本', '全球', '全美', '南美', '韩', '法国', '戛纳', '瑞士', '印尼', '智利', '老挝', '巴西', '印度', '新加坡', '泰', '首尔', '东京', '英国', '希腊', '美国'}
    
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
            WeeklyNews.res_append(News.objects.filter(publish_time__icontains=now), res_china, res_global)
        
        return 0, end_date.strftime('%Y-%m-%d'), res_china, res_global

    @staticmethod
    def res_append(query, res_china, res_global):
        for a in query:
            china, title = True, a.title
            for oversea_key in WeeklyNews.OVERSEA_KEYS:
                if oversea_key in title:
                    china = False
                    break
            (res_china if china else res_global).append({
                'title': a.title,
                'body': a.context,
                'url': a.url,
                'publish_time': a.publish_time,
                'media_name': a.media,
                'img_url': a.img if a.img else '',
            })

