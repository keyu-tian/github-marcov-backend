import json
from datetime import datetime, timedelta

from django.views import View

from knowledge.models import Knowledge
from news.models import News, Rumor
from utils.meta_wrapper import JSR


class WeeklyNews(View):
    OVERSEA_KEYS = {
        '世界卫生', '世卫', '全球', '驻',
        '东南亚', '日本', '东京', '韩', '首尔', '朝鲜', '泰', '老挝',
        '印度', '印尼', '新加坡',
        '英格兰', '英国', '伦敦', '法国', '巴黎', '戛纳', '瑞士', '希腊', '美国', '全美', '北美', '澳',
        '智利', '巴西', '南美',
    }
    
    @JSR('status', 'date', 'china', 'global')
    def post(self, request):
        # new_news = news_spider()
        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != {'date'}:
            return 1, '', [], []
        res_china, res_global = [], []
        today_date = datetime.now().date()
        
        if kwargs['date'] == '':
            for dis in range(7):
                cur_date = today_date - timedelta(days=dis)
                WeeklyNews.res_append(News.objects.filter(publish_time=cur_date), res_china, res_global)
        else:
            try:
                someday_date = datetime.strptime(kwargs['date'].split('T')[0], '%Y-%m-%d').date()
                WeeklyNews.res_append(News.objects.filter(publish_time=someday_date), res_china, res_global)
            except:
                return 2, '', [], []
        
        return 0, today_date.strftime('%Y-%m-%d'), res_china, res_global
    
    @staticmethod
    def res_append(query, res_china, res_global):
        for a in query:
            a: News
            china, title = True, a.title
            for oversea_key in WeeklyNews.OVERSEA_KEYS:
                if oversea_key in title:
                    china = False
                    break
            (res_china if china else res_global).append({
                'title': a.title,
                'body': a.context,
                'url': a.url,
                'publish_time': a.publish_time.strftime('%Y-%m-%d'),
                'media_name': a.media,
                'img_url': a.img if a.img else '',
            })


class RumorList(View):
    @JSR('status', 'data')
    def post(self, request):
        res = []
        for a in Rumor.objects.all():
            res.append({
                'title': a.title,
                'summary': a.summary,
                'body': a.body,
            })
        return 0, res


class KnowledgeList(View):
    @JSR('status', 'data')
    def post(self, request):
        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != {'start'}:
            return 1, []
        try:
            start = int(kwargs['start'])
        except:
            return 1
        res_set = Knowledge.objects.all()[start: start + 12]
        res = [{
            'id': a.id,
            'title': a.title,
            'summary': a.body,
            'source': a.source,
        }for a in res_set]
        return res