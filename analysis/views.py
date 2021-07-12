from django.views import View

from meta_config import SPIDER_DATA_DIRNAME
from user.views import get_is_star
from utils.meta_wrapper import JSR
from utils.dict_ch import province_dict_ch
import datetime as dt
import json
import os

epidemic_start_date = dt.date(2021, 7, 1)


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
    @JSR('status', 'population', 'data', 'is_star')
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
                        'total': c['total']
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

