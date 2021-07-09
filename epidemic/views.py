from functools import reduce

from django.db.models import Q
from django.views import View
from utils.meta_wrapper import JSR
from utils.dict_ch import city_dict_ch, province_dict_ch
from utils.country_dict import country_dict
from risk.views import get_city_risk_level
from epidemic.models import HistoryEpidemicData
from country.models import *
from news.models import *
import json


def list_dict_duplicate_removal(data_list):
    run_function = lambda x, y: x if y in x else x + [y]
    return reduce(run_function, [[], ] + data_list)


class MapProvince(View):
    @JSR('status', 'province')
    def post(self, request):
        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != {'name', 'date'}:
            return 1, []
        kwargs['name'] = province_dict_ch[kwargs['name']]
        province = {}
        data = HistoryEpidemicData.objects.filter(date=kwargs['date'], province_ch=kwargs['name'])
        if data.count() == 0:
            return 6, province
        province_data = data.first()
        province['new'] = {
            'died': province_data.province_new_died if province_data.province_new_died else 0,
            'cured': province_data.province_new_cured if province_data.province_new_cured else 0,
            'confirmed': province_data.province_new_confirmed if province_data.province_new_confirmed else 0
        }
        province['total'] = {
            'died': province_data.province_total_died if province_data.province_total_died else 0,
            'cured': province_data.province_total_cured if province_data.province_total_cured else 0,
            'confirmed': province_data.province_total_confirmed if province_data.province_total_confirmed else 0
        }
        cities = []
        # msg = Policy.objects.filter(city_name=province_data.province_ch)
        # if msg.count() == 0:
        #     msg = '未知'
        # else:
        #     msg = msg.first().enter_policy+'\n'+msg.first().out_policy
        infos = []
        policy_count = 0
        for city_data in data:
            city = {'name': city_data.city_ch}
            city['new'] = {
                'died': city_data.city_new_died if city_data.city_new_died else 0,
                'cured': city_data.city_new_cured if city_data.city_new_cured else 0,
                'confirmed': city_data.city_new_confirmed if city_data.city_new_confirmed else 0
            }
            city['total'] = {
                'died': city_data.city_total_died if city_data.city_total_died else 0,
                'cured': city_data.city_total_cured if city_data.city_total_cured else 0,
                'confirmed': city_data.city_total_confirmed if city_data.city_total_confirmed else 0,
            }
            cities.append(city)
            msg = Policy.objects.filter(city_name=city_data.city_ch)
            if msg.count() != 0:
                msg = f'进入{ city_data.city_ch }管控政策：{ msg.first().enter_policy }\n离开{ city_data.city_ch }管控政策：{ msg.first().out_policy }'
                info = {'level': get_city_risk_level(city_data.city_ch), 'msg': msg}
                infos.append(info)
            news_list = News.objects.filter(Q(title__icontains=city_data.city_ch) |
                                            Q(context__icontains=city_data.city_ch))
            for news in news_list:
                info = {'level': get_city_risk_level(city_data.city_ch), 'msg': news.title + '：' + news.context}
                infos.append(info)
        infos = list_dict_duplicate_removal(infos)
        province['cities'] = cities
        province['info'] = infos
        return 0, province


class MapProvinceDt(View):
    @JSR('status', 'data')
    def post(self, request):
        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != {'name'}:
            return 1, []
        kwargs['name'] = country_dict[kwargs['name']]
        total_data = HistoryEpidemicData.objects.filter(province_ch=kwargs['name'])
        res = []
        date = []
        for province_data in total_data:
            if province_data.date in date:
                continue
            data = {'date': province_data.date}
            date.append(province_data.date)
            data['new'] = {
                'died': province_data.province_new_died if province_data.province_new_died else 0,
                'cured': province_data.province_new_cured if province_data.province_new_cured else 0,
                'confirmed': province_data.province_new_confirmed if province_data.province_new_confirmed else 0
            }
            data['total'] = {
                'died': province_data.province_total_died if province_data.province_total_died else 0,
                'cured': province_data.province_total_cured if province_data.province_total_cured else 0,
                'confirmed': province_data.province_total_confirmed if province_data.province_total_confirmed else 0
            }
            res.append(data)
        return 0, res


class MapOversea(View):
    @JSR('status', 'country')
    def post(self, request):
        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != {'name', 'date'}:
            return 1, []
        kwargs['name'] = list(country_dict.keys())[list(country_dict.values()).index(kwargs['name'])]
        country = {}
        data = HistoryEpidemicData.objects.filter(date=kwargs['date'], country_ch=kwargs['name'])
        if data.count() == 0:
            return 6, country
        country['new'] = {
            'died': 0,
            'cured': 0,
            'confirmed': 0
        }
        country['total'] = {
            'died': 0,
            'cured': 0,
            'confirmed': 0
        }
        states = []
        infos = []
        for state_data in data:
            # msg = Policy.objects.filter(city_name=state_data.city_ch)
            # if msg.count() == 0:
            #     msg = '未知'
            # else:
            #     msg = msg.first().enter_policy+'\n'+msg.first().out_policy
            info = {'level': get_city_risk_level(state_data.city_ch), 'msg': '未知'}
            state = {'name': state_data.state_en if state_data.state_en else ''}
            state['new'] = {
                'died': state_data.city_new_died if state_data.city_new_died else 0,
                'cured': state_data.city_new_cured if state_data.city_new_cured else 0,
                'confirmed': state_data.city_new_confirmed if state_data.city_new_confirmed else 0
            }
            country['new']['died'] += state['new']['died']
            country['new']['cured'] += state['new']['cured']
            country['new']['confirmed'] += state['new']['confirmed']
            state['total'] = {
                'died': state_data.city_total_died if state_data.city_total_died else 0,
                'cured': state_data.city_total_cured if state_data.city_total_cured else 0,
                'confirmed': state_data.city_total_confirmed if state_data.city_total_confirmed else 0,
            }
            country['total']['died'] += state['total']['died']
            country['total']['cured'] += state['total']['cured']
            country['total']['confirmed'] += state['total']['confirmed']
            states.append(state)
            infos.append(info)
        country['states'] = states
        country['info'] = infos
        return 0, country


class MapOverseaDt(View):
    @JSR('status', 'data')
    def post(self, request):
        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != {'name'}:
            return 1, []
        kwargs['name'] = list(country_dict.keys())[list(country_dict.values()).index(kwargs['name'])]
        country = {}
        total_data = HistoryEpidemicData.objects.filter(country_ch=kwargs['name'])
        if total_data.count() == 0:
            return 6, country
        date = []
        for state_data in total_data:
            if state_data.date not in date:
                country[state_data.date] = {}
                date.append(state_data.date)
                country[state_data.date]['new'] = {
                    'died': 0,
                    'cured': 0,
                    'confirmed': 0
                }
                country[state_data.date]['total'] = {
                    'died': 0,
                    'cured': 0,
                    'confirmed': 0
                }
            state = {}
            state['new'] = {
                'died': state_data.city_new_died if state_data.city_new_died else 0,
                'cured': state_data.city_new_cured if state_data.city_new_cured else 0,
                'confirmed': state_data.city_new_confirmed if state_data.city_new_confirmed else 0
            }
            country[state_data.date]['new']['died'] += state['new']['died']
            country[state_data.date]['new']['cured'] += state['new']['cured']
            country[state_data.date]['new']['confirmed'] += state['new']['confirmed']
            state['total'] = {
                'died': state_data.city_total_died if state_data.city_total_died else 0,
                'cured': state_data.city_total_cured if state_data.city_total_cured else 0,
                'confirmed': state_data.city_total_confirmed if state_data.city_total_confirmed else 0,
            }
            country[state_data.date]['total']['died'] += state['total']['died']
            country[state_data.date]['total']['cured'] += state['total']['cured']
            country[state_data.date]['total']['confirmed'] += state['total']['confirmed']
        dates = list(country.keys())
        res = []
        for d in dates:
            res.append({'date': d, 'new': country[d]['new'], 'total': country[d]['total']})
        return 0, res


class MapOversea(View):
    @JSR('status', 'country')
    def post(self, request):
        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != {'name', 'date'}:
            return 1, []
        kwargs['name'] = list(country_dict.keys())[list(country_dict.values()).index(kwargs['name'])]
        country = {}
        data = HistoryEpidemicData.objects.filter(date=kwargs['date'], country_ch=kwargs['name'])
        if data.count() == 0:
            return 6, country
        country['new'] = {
            'died': 0,
            'cured': 0,
            'confirmed': 0
        }
        country['total'] = {
            'died': 0,
            'cured': 0,
            'confirmed': 0
        }
        states = []
        infos = []
        for state_data in data:
            # msg = Policy.objects.filter(city_name=state_data.city_ch)
            # if msg.count() == 0:
            #     msg = '未知'
            # else:
            #     msg = msg.first().enter_policy+'\n'+msg.first().out_policy
            info = {'level': get_city_risk_level(state_data.city_ch), 'msg': '未知'}
            state = {'name': state_data.state_en}
            state['new'] = {
                'died': state_data.city_new_died if state_data.city_new_died else 0,
                'cured': state_data.city_new_cured if state_data.city_new_cured else 0,
                'confirmed': state_data.city_new_confirmed if state_data.city_new_confirmed else 0
            }
            country['new']['died'] += state['new']['died']
            country['new']['cured'] += state['new']['cured']
            country['new']['confirmed'] += state['new']['confirmed']
            state['total'] = {
                'died': state_data.city_total_died if state_data.city_total_died else 0,
                'cured': state_data.city_total_cured if state_data.city_total_cured else 0,
                'confirmed': state_data.city_total_confirmed if state_data.city_total_confirmed else 0,
            }
            country['total']['died'] += state['total']['died']
            country['total']['cured'] += state['total']['cured']
            country['total']['confirmed'] += state['total']['confirmed']
            states.append(state)
            infos.append(info)
        country['states'] = states
        country['info'] = infos
        return 0, country


class MapOverseaDt(View):
    @JSR('status', 'data')
    def post(self, request):
        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != {'name'}:
            return 1, []
        kwargs['name'] = list(country_dict.keys())[list(country_dict.values()).index(kwargs['name'])]
        country = {}
        total_data = HistoryEpidemicData.objects.filter(country_ch=kwargs['name'])
        if total_data.count() == 0:
            return 6, country
        date = []
        for state_data in total_data:
            if state_data.date not in date:
                country[state_data.date] = {}
                date.append(state_data.date)
                country[state_data.date]['new'] = {
                    'died': 0,
                    'cured': 0,
                    'confirmed': 0
                }
                country[state_data.date]['total'] = {
                    'died': 0,
                    'cured': 0,
                    'confirmed': 0
                }
            state = {}
            state['new'] = {
                'died': state_data.city_new_died if state_data.city_new_died else 0,
                'cured': state_data.city_new_cured if state_data.city_new_cured else 0,
                'confirmed': state_data.city_new_confirmed if state_data.city_new_confirmed else 0
            }
            country[state_data.date]['new']['died'] += state['new']['died']
            country[state_data.date]['new']['cured'] += state['new']['cured']
            country[state_data.date]['new']['confirmed'] += state['new']['confirmed']
            state['total'] = {
                'died': state_data.city_total_died if state_data.city_total_died else 0,
                'cured': state_data.city_total_cured if state_data.city_total_cured else 0,
                'confirmed': state_data.city_total_confirmed if state_data.city_total_confirmed else 0,
            }
            country[state_data.date]['total']['died'] += state['total']['died']
            country[state_data.date]['total']['cured'] += state['total']['cured']
            country[state_data.date]['total']['confirmed'] += state['total']['confirmed']
        dates = list(country.keys())
        res = []
        for d in dates:
            res.append({'date': d, 'new': country[d]['new'], 'total': country[d]['total']})
        return 0, res


class MapOversea(View):
    @JSR('status', 'country')
    def post(self, request):
        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != {'name', 'date'}:
            return 1, []
        kwargs['name'] = list(country_dict.keys())[list(country_dict.values()).index(kwargs['name'])]
        country = {}
        data = HistoryEpidemicData.objects.filter(date=kwargs['date'], country_ch=kwargs['name'])
        if data.count() == 0:
            return 6, country
        country['new'] = {
            'died': 0,
            'cured': 0,
            'confirmed': 0
        }
        country['total'] = {
            'died': 0,
            'cured': 0,
            'confirmed': 0
        }
        states = []
        infos = []
        for state_data in data:
            # msg = Policy.objects.filter(city_name=state_data.city_ch)
            # if msg.count() == 0:
            #     msg = '未知'
            # else:
            #     msg = msg.first().enter_policy+'\n'+msg.first().out_policy
            info = {'level': get_city_risk_level(state_data.city_ch), 'msg': '未知'}
            state = {'name': state_data.state_en}
            state['new'] = {
                'died': state_data.city_new_died if state_data.city_new_died else 0,
                'cured': state_data.city_new_cured if state_data.city_new_cured else 0,
                'confirmed': state_data.city_new_confirmed if state_data.city_new_confirmed else 0
            }
            country['new']['died'] += state['new']['died']
            country['new']['cured'] += state['new']['cured']
            country['new']['confirmed'] += state['new']['confirmed']
            state['total'] = {
                'died': state_data.city_total_died if state_data.city_total_died else 0,
                'cured': state_data.city_total_cured if state_data.city_total_cured else 0,
                'confirmed': state_data.city_total_confirmed if state_data.city_total_confirmed else 0,
            }
            country['total']['died'] += state['total']['died']
            country['total']['cured'] += state['total']['cured']
            country['total']['confirmed'] += state['total']['confirmed']
            states.append(state)
            infos.append(info)
        country['states'] = states
        country['info'] = infos
        return 0, country


class MapOverseaDt(View):
    @JSR('status', 'data')
    def post(self, request):
        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != {'name'}:
            return 1, []
        kwargs['name'] = list(country_dict.keys())[list(country_dict.values()).index(kwargs['name'])]
        country = {}
        total_data = HistoryEpidemicData.objects.filter(country_ch=kwargs['name'])
        if total_data.count() == 0:
            return 6, country
        date = []
        for state_data in total_data:
            if state_data.date not in date:
                country[state_data.date] = {}
                date.append(state_data.date)
                country[state_data.date]['new'] = {
                    'died': 0,
                    'cured': 0,
                    'confirmed': 0
                }
                country[state_data.date]['total'] = {
                    'died': 0,
                    'cured': 0,
                    'confirmed': 0
                }
            state = {}
            state['new'] = {
                'died': state_data.city_new_died if state_data.city_new_died else 0,
                'cured': state_data.city_new_cured if state_data.city_new_cured else 0,
                'confirmed': state_data.city_new_confirmed if state_data.city_new_confirmed else 0
            }
            country[state_data.date]['new']['died'] += state['new']['died']
            country[state_data.date]['new']['cured'] += state['new']['cured']
            country[state_data.date]['new']['confirmed'] += state['new']['confirmed']
            state['total'] = {
                'died': state_data.city_total_died if state_data.city_total_died else 0,
                'cured': state_data.city_total_cured if state_data.city_total_cured else 0,
                'confirmed': state_data.city_total_confirmed if state_data.city_total_confirmed else 0,
            }
            country[state_data.date]['total']['died'] += state['total']['died']
            country[state_data.date]['total']['cured'] += state['total']['cured']
            country[state_data.date]['total']['confirmed'] += state['total']['confirmed']
        dates = list(country.keys())
        res = []
        for d in dates:
            res.append({'date': d, 'new': country[d]['new'], 'total': country[d]['total']})
        return 0, res
