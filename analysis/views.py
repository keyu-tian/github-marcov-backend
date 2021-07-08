from django.views import View
from django.db.models import Q

from meta_config import IMPORTER_DATA_DIRNAME
from utils.meta_wrapper import JSR
from utils.dict_ch import province_dict_ch, province_population
from utils.country_dict import country_dict, country_population
from epidemic.models import HistoryEpidemicData
import datetime as dt
import json
import os

epidemic_start_date = dt.date(2021, 7, 1)


class DomesticAnalyze(View):
    @JSR('status', 'data')
    def get(self, request):
        try:
            json_path = os.path.join(IMPORTER_DATA_DIRNAME, 'epidemic_domestic_data', 'province.json')
            analysis = json.load(open(json_path, 'r', encoding='utf-8'))
        except:
            return 7
        return 0, analysis


class DomesticTodayAnalyze(View):
    @JSR('status', 'data')
    def get(self, request):
        try:
            json_path = os.path.join(IMPORTER_DATA_DIRNAME, 'epidemic_domestic_data', 'province.json')
            analysis = json.load(open(json_path, 'r', encoding='utf-8'))
        except:
            return 7
        return 0, [analysis[-1]]


class InternationalAnalyze(View):
    @JSR('status', 'data')
    def get(self, request):
        # json_path = os.path.join('spiders_data', 'epidemic_domestic_data', 'province.json')
        try:
            json_path = os.path.join(IMPORTER_DATA_DIRNAME, 'global.json')
            analysis = json.load(open(json_path, 'r', encoding='utf-8'))
        except:
            return 7
        return 0, analysis


class InternationalTodayAnalyze(View):
    @JSR('status', 'data')
    def get(self, request):
        # json_path = os.path.join('spiders_data', 'epidemic_domestic_data', 'province.json')
        try:
            json_path = os.path.join(IMPORTER_DATA_DIRNAME, 'global.json')
            analysis = json.load(open(json_path, 'r', encoding='utf-8'))
        except:
            return 7
        return 0, [analysis[-1]]


class SearchAnalyse(View):
    @JSR('status', 'population', 'data')
    def post(self, request):
        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != {'name'}:
            return 1, []

        try:
            global_json_path = os.path.join(IMPORTER_DATA_DIRNAME, 'global.json')
            province_json_path = os.path.join(IMPORTER_DATA_DIRNAME, 'epidemic_domestic_data', 'province.json')
        except:
            return 7

        #TODO: 未测试
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
                            'total_confirmed': c['total']['confirmed']
                        })
        else:
            global_analysis = json.load(open(global_json_path, 'r', encoding='utf-8'))
            for d in global_analysis:
                for c in d['country']:
                    if c['name'] == kwargs['name']:
                        daily_data.append({
                            'date': d['date'],
                            'total_died': c['total']['died'],
                            'total_cured': c['total']['cured'],
                            'total_confirmed': c['total']['confirmed']
                        })


        """
        name_dict = {}
        for it in country_dict.items():
            name_dict[it[1]] = it[0]
        try:
            if kwargs['name'] in province_dict_ch.keys():
                epidemics = HistoryEpidemicData.objects.filter(province_ch__exact=province_dict_ch[kwargs['name']])
                population = province_population.get(kwargs['name'], '未知')
            else:
                epidemics = HistoryEpidemicData.objects.filter(country_ch__exact=name_dict[kwargs['name']])
                population = '未知'
                for it in country_population.items():
                    # TODO: 查询国家人口模糊匹配
                    if it[0] == name_dict[kwargs['name']]:
                        population = it[1]
        except:
            return 7
        
        daily_data = {}
        for epidemic in epidemics:
            if epidemic.date not in daily_data.keys():
                daily_data[epidemic.date] = {
                    'date': epidemic.date,
                    'total_died': 0,
                    'total_cured': 0,
                    'total_confirmed': 0
                }
            if kwargs['name'] in province_dict_ch.keys():
                daily_data[epidemic.date] = {
                    'date': epidemic.date,
                    'total_died': max(epidemic.province_total_died, daily_data[epidemic.date]['total_died']),
                    'total_cured': max(epidemic.province_total_cured, daily_data[epidemic.date]['total_cured']),
                    'total_confirmed': max(epidemic.province_total_confirmed, daily_data[epidemic.date]['total_confirmed'])
                }
            else:
                daily_data[epidemic.date] = {
                    'date': epidemic.date,
                    'total_died': epidemic.province_total_died + daily_data[epidemic.date]['total_died'],
                    'total_cured': epidemic.province_total_cured + daily_data[epidemic.date]['total_cured'],
                    'total_confirmed': epidemic.province_total_confirmed + daily_data[epidemic.date]['total_confirmed']
                }
        """


        return 0, population, daily_data


class CountryAnalyze(View):
    @JSR('status', 'population', 'data')
    def post(self, request):
        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != {'name'}:
            return 1, []


        try:
            global_json_path = os.path.join(IMPORTER_DATA_DIRNAME, 'global.json')
            province_json_path = os.path.join(IMPORTER_DATA_DIRNAME, 'epidemic_domestic_data', 'province.json')
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
                            'new': c['new'],
                            'total': c['total']
                        })
        else:
            global_analysis = json.load(open(global_json_path, 'r', encoding='utf-8'))
            for d in global_analysis:
                for c in d['countries']:
                    if c['name'] == kwargs['name']:
                        daily_data.append({
                            'date': d['date'],
                            'new': c['new'],
                            'total': c['total']
                        })

        '''
        name_dict = {}
        for it in country_dict.items():
            name_dict[it[1]] = it[0]
        try:
            if kwargs['name'] in province_dict_ch.keys():
                epidemics = HistoryEpidemicData.objects.filter(province_ch__exact=province_dict_ch[kwargs['name']])
                population = province_population.get(kwargs['name'], '未知')
            else:
                epidemics = HistoryEpidemicData.objects.filter(country_ch__exact=name_dict[kwargs['name']])
                population = '未知'
                for it in country_population.items():
                    # TODO: 查询国家人口模糊匹配
                    if it[0] == name_dict[kwargs['name']]:
                        population = it[1]
        except:
            return 7

        daily_data = {}
        for epidemic in epidemics:
            if epidemic.date not in daily_data.keys():
                daily_data[epidemic.date] = {
                    'date': epidemic.date,
                    'total': {
                        'died': 0,
                        'cured': 0,
                        'confirmed': 0
                    },
                    'new': {
                        'died': 0,
                        'cured': 0,
                        'confirmed': 0
                    }
                }
            if kwargs['name'] in province_dict_ch.keys():
                daily_data[epidemic.date] = {
                    'date': epidemic.date,
                    'total': {
                        'died': max(epidemic.province_total_died, daily_data[epidemic.date]['total']['died']),
                        'cured': max(epidemic.province_total_cured, daily_data[epidemic.date]['total']['cured']),
                        'confirmed': max(epidemic.province_total_confirmed, daily_data[epidemic.date]['total']['confirmed'])
                    },
                    'new': {
                        'died': max(epidemic.province_new_died, daily_data[epidemic.date]['new']['died']),
                        'cured': max(epidemic.province_new_cured, daily_data[epidemic.date]['new']['cured']),
                        'confirmed': max(epidemic.province_new_confirmed, daily_data[epidemic.date]['new']['confirmed'])
                    }
                }
            else:
                daily_data[epidemic.date] = {
                    'date': epidemic.date,
                    'total': {
                        'died': epidemic.province_total_died + daily_data[epidemic.date]['total']['died'],
                        'cured': epidemic.province_total_cured + daily_data[epidemic.date]['total']['cured'],
                        'confirmed': epidemic.province_total_confirmed + daily_data[epidemic.date]['total']['confirmed']
                    },
                    'new': {
                        'died': epidemic.province_new_died + daily_data[epidemic.date]['new']['died'],
                        'cured': epidemic.province_new_cured + daily_data[epidemic.date]['new']['cured'],
                        'confirmed': epidemic.province_new_confirmed + daily_data[epidemic.date]['new']['confirmed']
                    }
                }
        '''
        return 0, population, daily_data


class CountryList(View):
    @JSR('status', 'names')
    def get(self, request):
        return 0, list(country_dict.values())


class ProvinceList(View):
    @JSR('status', 'names')
    def get(self, request):
        return 0, list(province_dict_ch.keys())[:-1]