import datetime

from django.views import View

from meta_config import SPIDER_DATA_DIRNAME
from spiders.epidemic_global_importer import dt_delta
from user.models import User, Follow
from utils.country_dict import country_dict
from utils.meta_wrapper import JSR
from utils.dict_ch import province_dict_ch, vaccine
import datetime as dt
import json
import os

epidemic_start_date = dt.date(2021, 7, 1)


def get_is_star(request, level, country='', province='', city=''):
    try:
        uid = int(request.session.get('uid', None))
        user = User.objects.get(id=uid)
    except:
        return 2

    follow_set = Follow.objects.filter(user=user)
    if level == 1:
        if follow_set.filter(level=1, country=country).exists():
            return 1
        else:
            return 0
    elif level == 2:
        if follow_set.filter(level=2, province=province).exists():
            return 1
        else:
            return 0
    elif level == 3:
        if follow_set.filter(level=3, province=province, city=city).exists():
            return 1
        else:
            return 0
    else:
        if follow_set.filter(level=1, country=country).exists() or follow_set.filter(level=2,
                                                                                     province=country).exists():
            return 1
        else:
            return 0


class DomesticAnalyze(View):
    @JSR('status', 'data')
    def get(self, request):
        try:
            json_path = os.path.join(SPIDER_DATA_DIRNAME, 'epidemic_domestic_data', 'province.json')
            analysis = json.load(open(json_path, 'r', encoding='utf-8'))
        except:
            return 7
        return 0, analysis


class DomesticTodayAnalyze(View):
    @JSR('status', 'data')
    def get(self, request):
        try:
            json_path = os.path.join(SPIDER_DATA_DIRNAME, 'epidemic_domestic_data', 'province.json')
            analysis = json.load(open(json_path, 'r', encoding='utf-8'))
        except:
            return 7
        return 0, [analysis[-1]]


class InternationalAnalyze(View):
    @JSR('status', 'data', 'today')
    def get(self, request):
        # json_path = os.path.join('spiders_data', 'epidemic_domestic_data', 'province.json')
        try:
            json_path = os.path.join(SPIDER_DATA_DIRNAME, 'global.json')
            analysis = json.load(open(json_path, 'r', encoding='utf-8'))
        except:
            return 7
        return 0, analysis[:-1], analysis[-1]


class InternationalTodayAnalyze(View):
    @JSR('status', 'data', 'today')
    def get(self, request):
        # json_path = os.path.join('spiders_data', 'epidemic_domestic_data', 'province.json')
        try:
            json_path = os.path.join(SPIDER_DATA_DIRNAME, 'global.json')
            analysis = json.load(open(json_path, 'r', encoding='utf-8'))
        except:
            return 7
        return 0, [analysis[-2]], analysis[-1]


class InternationalFutureAnalyze(View):
    @JSR('status', 'data')
    def get(self, request):
        # json_path = os.path.join('spiders_data', 'epidemic_domestic_data', 'province.json')
        try:
            json_path = os.path.join(SPIDER_DATA_DIRNAME, 'predict.json')
            analysis = json.load(open(json_path, 'r', encoding='utf-8'))
        except:
            return 7
        return 0, analysis


class SearchAnalyse(View):
    @JSR('status', 'population', 'data')
    def post(self, request):
        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != {'name'}:
            return 1, []

        try:
            global_json_path = os.path.join(SPIDER_DATA_DIRNAME, 'global.json')
            province_json_path = os.path.join(SPIDER_DATA_DIRNAME, 'epidemic_domestic_data', 'province.json')
        except:
            return 7

        population = 0
        daily_data = []
        if kwargs['name'] in province_dict_ch.keys():
            province_analysis = json.load(open(province_json_path, 'r', encoding='utf-8'))
            for d in province_analysis:
                for c in d['provinces']:
                    if c['name'] == kwargs['name']:
                        daily_data.append({
                            'date': d['date'],
                            'total_died': c['total']['died'],
                            'total_cured': c['total']['cured'],
                            'total_confirmed': c['total']['confirmed'],
                        })
        else:
            global_analysis = json.load(open(global_json_path, 'r', encoding='utf-8'))
            for d in global_analysis[:-1]:
                for c in d['countries']:
                    if c['name'] == kwargs['name']:
                        info = {
                            'date': d['date'],
                            'total_died': c['total']['died'],
                            'total_cured': c['total']['cured'],
                            'total_confirmed': c['total']['confirmed'],
                        }
                        if c['total']['vaccinated'] != "未知":
                            info['total_vaccinated'] = c['total']['vaccinated']
                        daily_data.append(info)

        return 0, population, daily_data


class CountryAnalyze(View):
    @JSR('status', 'population', 'data')
    def post(self, request):
        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != {'name'}:
            return 1, []
        population, daily_data = country_analyse_data_res(kwargs)
        if population is None and daily_data is None:
            return 7
        return 0, population, daily_data, get_is_star(request, level=4, country=kwargs['name'])


def country_analyse_data_res(kwargs):
    try:
        global_json_path = os.path.join(SPIDER_DATA_DIRNAME, 'global.json')
        province_json_path = os.path.join(SPIDER_DATA_DIRNAME, 'epidemic_domestic_data', 'province.json')
    except:
        return None, None

    population = 0
    daily_data = []
    if kwargs['name'] in province_dict_ch.keys():
        province_analysis = json.load(open(province_json_path, 'r', encoding='utf-8'))
        for d in province_analysis:
            for c in d['provinces']:
                if c['name'] == kwargs['name']:
                    daily_data.append({
                        'date': d['date'],
                        'new': c['new'],
                        'total': {
                            'confirmed': c['total']['confirmed'],
                            'died': c['total']['died'],
                            'cured': c['total']['cured'],
                            'vaccinated': vaccine[kwargs['name']],
                        }
                    })
    else:
        global_analysis = json.load(open(global_json_path, 'r', encoding='utf-8'))
        for d in global_analysis[:-1]:
            for c in d['countries']:
                if c['name'] == kwargs['name']:
                    daily_data.append({
                        'date': d['date'],
                        'new': c['new'],
                        'total': c['total']
                    })

    return population, daily_data


def get_country_info(country):
    if country not in country_dict.values():
        return "没有该国家信息"
    else:
        with open(os.path.join(SPIDER_DATA_DIRNAME, "true_data.json"), "r", encoding="utf-8") as f:
            data = json.load(f)
            date = datetime.date.today() + datetime.timedelta(-1)
            msg = "截至%s年%s月%s日，%s现有确诊%s人、治愈%s人、死亡%s人，较前一日新增确诊%s人、新增治愈%s人、新增死亡%s人" \
                  % (str(date.year), str(date.month), str(date.day),
                     country,
                     data[country]["confirmed"],
                     data[country]["cured"],
                     data[country]["died"],
                     data[country]["new_confirmed"],
                     data[country]["new_cured"],
                     data[country]["new_died"],)
            return msg


def get_province_info(province):
    if province not in province_dict_ch.keys():
        return "没有该省信息"
    else:
        with open(os.path.join(SPIDER_DATA_DIRNAME, "epidemic_domestic_data", "province.json"), "r",
                  encoding="utf-8") as f:
            data = json.load(f)
            provinces_data = data[-1]
            date = provinces_data['date'].split('-')
            for province_data in provinces_data['provinces']:
                if province_data['name'] == province:
                    msg = "截至%s年%s月%s日，%s现有确诊%s人、治愈%s人、死亡%s人，较前一日新增确诊%s人、新增治愈%s人、新增死亡%s人" \
                          % (date[0], date[1], date[2],
                             province,
                             province_data['total']["confirmed"],
                             province_data['total']["cured"],
                             province_data['total']["died"],
                             province_data['new']["confirmed"],
                             province_data['new']["cured"],
                             province_data['new']["died"])
                    return msg
