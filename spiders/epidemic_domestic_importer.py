# -*- coding: utf-8 -*-

import datetime as dt
import json
import os
import re
from datetime import datetime

from meta_config import IMPORTER_DATA_DIRNAME
from utils.dict_ch import province_dict_ch, province_population
from epidemic.models import HistoryEpidemicData


def epidemic_domestic_import(to_database=False, date_begin='2020-01-22', date_end='2021-07-08'):
    global title, city

    date_begin = date_begin.split('-')
    date_end = date_end.split('-')
    begin = dt.date(int(date_begin[0]), int(date_begin[1]), int(date_begin[2]))
    end = dt.date(int(date_end[0]), int(date_end[1]), int(date_end[2]))

    input_file = os.path.join(IMPORTER_DATA_DIRNAME, 'epidemic_domestic_data', 'DXYArea.csv')  # "t15.csv"
    csv_download_path = os.path.join(IMPORTER_DATA_DIRNAME, 'epidemic_domestic_data', 'DXYArea.csv')
    area_file = os.path.join(IMPORTER_DATA_DIRNAME, 'epidemic_domestic_data', 'area.json')
    json_file = os.path.join(IMPORTER_DATA_DIRNAME, 'epidemic_domestic_data', 'province.json')
    out_title = [
        'country_ch', 'province_ch', 'city_ch', 'province_total_died', 'province_total_cured',
        'province_total_confirmed', 'province_new_died', 'province_new_cured', 'province_new_confirmed',
        'city_total_died', 'city_total_cured', 'city_total_confirmed', 'city_new_died', 'city_new_cured',
        'city_new_confirmed'
    ]

    # TODO: 获取当天数据
    # os.system('wget https://github.com/BlankerL/DXY-COVID-19-Data/releases/download/%s/DXYArea.csv --no-check-certificate -o ' % (dt.datetime.strftime(dt.date.today(), '%Y.%m.%d')) + csv_download_path)

    f = open(input_file, "r", encoding='utf-8')
    title = f.readline()[:-1].split(',')
    all_data = []
    for line in f:
        single_data = {}
        ls = re.split(',(?!\\s)', line[:-1])
        if ls[2] != '中国':
            continue
        for it in zip(title, ls):
            if 'Count' in it[0]:
                try:
                    single_data[it[0]] = int(it[1])
                except:
                    single_data[it[0]] = 0
            else:
                single_data[it[0]] = it[1]
        if '境外输入' in single_data['cityName']:
            single_data['cityName'] += '-' + single_data['provinceName']
        if '不明' in single_data['cityName']:
            single_data['cityName'] += '-' + single_data['provinceName']
        if '待明确' in single_data['cityName']:
            single_data['cityName'] += '-' + single_data['provinceName']
        if single_data['cityName'] == '':
            single_data['cityName'] = single_data['provinceName']
        single_data['updateTime'] = datetime.strptime(single_data['updateTime'].split(' ')[0].replace('/', '-'), '%Y-%m-%d')
        single_data['updateTime'] = datetime.strftime(single_data['updateTime'], '%Y-%m-%d')
        all_data.append(single_data)
    all_data.reverse()

    daily_info = {}
    last = json.load(open(area_file))
    for city in last.keys():
        last[city]['province_total_died'] = 0
        last[city]['province_total_cured'] = 0
        last[city]['province_total_confirmed'] = 0
        last[city]['city_total_died'] = 0
        last[city]['city_total_cured'] = 0
        last[city]['city_total_confirmed'] = 0

    delta = dt.timedelta(days=1)
    d = begin
    analysis = []
    idx = 0
    while all_data[idx]['updateTime'] != d.strftime('%Y-%m-%d'):
        idx += 1
    while d <= end:
        nd = d.strftime('%Y-%m-%d')
        print(nd)
        daily_info[nd] = {}
        for city in last.keys():
            daily_info[nd][city] = {}
            daily_info[nd][city]['country_ch'] = last[city]['countryName']
            daily_info[nd][city]['province_ch'] = last[city]['provinceName']
            daily_info[nd][city]['city_ch'] = city
            daily_info[nd][city]['province_total_died'] = last[city]['province_total_died']
            daily_info[nd][city]['province_total_cured'] = last[city]['province_total_cured']
            daily_info[nd][city]['province_total_confirmed'] = last[city]['province_total_confirmed']
            daily_info[nd][city]['province_new_died'] = 0
            daily_info[nd][city]['province_new_cured'] = 0
            daily_info[nd][city]['province_new_confirmed'] = 0
            daily_info[nd][city]['city_total_died'] = last[city]['city_total_died']
            daily_info[nd][city]['city_total_cured'] = last[city]['city_total_cured']
            daily_info[nd][city]['city_total_confirmed'] = last[city]['city_total_confirmed']
            daily_info[nd][city]['city_new_died'] = 0
            daily_info[nd][city]['city_new_cured'] = 0
            daily_info[nd][city]['city_new_confirmed'] = 0

        while idx < len(all_data) and all_data[idx]['updateTime'] == nd:
            for city in last.keys():
                if all_data[idx]['provinceName'] == last[city]['provinceName']:
                    daily_info[nd][city]['province_new_died'] = max(
                        all_data[idx]['province_deadCount'] - last[city]['province_total_died'], 0)
                    daily_info[nd][city]['province_new_cured'] = max(
                        all_data[idx]['province_curedCount'] - last[city]['province_total_cured'], 0)
                    daily_info[nd][city]['province_new_confirmed'] = max(
                        all_data[idx]['province_confirmedCount'] - last[city]['province_total_confirmed'], 0)
                    daily_info[nd][city]['province_total_died'] = max(
                        all_data[idx]['province_deadCount'], 0)
                    daily_info[nd][city]['province_total_cured'] = max(
                        all_data[idx]['province_curedCount'], 0)
                    daily_info[nd][city]['province_total_confirmed'] = max(
                        all_data[idx]['province_confirmedCount'], 0)

            city = all_data[idx]['cityName']
            daily_info[nd][city]['city_new_died'] = max(
                all_data[idx]['city_deadCount'] - last[city]['city_total_died'], 0)
            daily_info[nd][city]['city_new_cured'] = max(
                all_data[idx]['city_curedCount'] - last[city]['city_total_cured'], 0)
            daily_info[nd][city]['city_new_confirmed'] = max(
                all_data[idx]['city_confirmedCount'] - last[city]['city_total_confirmed'], 0)
            daily_info[nd][city]['city_total_died'] = max(
                all_data[idx]['city_deadCount'], 0)
            daily_info[nd][city]['city_total_cured'] = max(
                all_data[idx]['city_curedCount'], 0)
            daily_info[nd][city]['city_total_confirmed'] = max(
                all_data[idx]['city_confirmedCount'], 0)

            idx += 1

        for city in last.keys():
            for city2 in last.keys():
                if last[city]['provinceName'] == last[city2]['provinceName']:
                    last[city]['province_total_died'] = max(daily_info[nd][city2]['province_total_died'], 0)
                    last[city]['province_total_cured'] = max(daily_info[nd][city2]['province_total_cured'], 0)
                    last[city]['province_total_confirmed'] = max(daily_info[nd][city2]['province_total_confirmed'], 0)
            last[city]['city_total_died'] = max(daily_info[nd][city]['city_total_died'], 0)
            last[city]['city_total_cured'] = max(daily_info[nd][city]['city_total_cured'], 0)
            last[city]['city_total_confirmed'] = max(daily_info[nd][city]['city_total_confirmed'], 0)

        if to_database:
            objs = []
            for it in daily_info[nd].items():
                dic = {'date': nd}
                for k in out_title:
                    dic[k] = it[1][k]
                objs.append(HistoryEpidemicData(**dic))
            HistoryEpidemicData.objects.bulk_create(objs)
        d += delta
    d = begin

    while d <= end:
        nd = d.strftime('%Y-%m-%d')
        daily_analysis = {'date': nd, 'provinces': []}
        for city_front, city in province_dict_ch.items():
            pd = {'name': city_front}
            for it in province_population.items():
                if it[0] in city:
                    pd['population'] = it[1]
            data_new = {'died': daily_info[nd][city]['province_new_died'],
                        'cured': daily_info[nd][city]['province_new_cured'],
                        'confirmed': daily_info[nd][city]['province_new_confirmed']}
            data_total = {'died': daily_info[nd][city]['province_total_died'],
                          'cured': daily_info[nd][city]['province_total_cured'],
                          'confirmed': daily_info[nd][city]['province_total_confirmed']}
            pd['new'] = data_new
            pd['total'] = data_total
            daily_analysis['provinces'].append(pd)
        analysis.append(daily_analysis)
        d += delta
    json.dump(analysis, open(json_file, 'w'), ensure_ascii=False)
