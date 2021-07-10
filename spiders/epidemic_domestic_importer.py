# -*- coding: utf-8 -*-

import datetime as dt
import json
import os
import re
from datetime import datetime

from tqdm import tqdm

from meta_config import IMPORTER_DATA_DIRNAME
from utils.dict_ch import province_dict_ch, province_population, city_dict_ch
from utils.download import download_from_url

delta = dt.timedelta(days=1)


# from spiders.epidemic_domestic_importer import epidemic_domestic_import
def epidemic_domestic_import(date_begin='2020-01-22',
                             date_end=datetime.strftime(datetime.today() - delta, '%Y-%m-%d')):
    # 正式版本参数中应为datetime.today()

    date_begin = date_begin.split('-')
    date_end = date_end.split('-')
    begin = dt.date(int(date_begin[0]), int(date_begin[1]), int(date_begin[2]))
    end = dt.date(int(date_end[0]), int(date_end[1]), int(date_end[2]))

    input_file = os.path.join(IMPORTER_DATA_DIRNAME, 'epidemic_domestic_data', 'DXYArea.csv')
    area_file = os.path.join(IMPORTER_DATA_DIRNAME, 'epidemic_domestic_data', 'area.json')
    province_json_file = os.path.join(IMPORTER_DATA_DIRNAME, 'epidemic_domestic_data', 'province.json')
    city_json_file_directory = os.path.join(IMPORTER_DATA_DIRNAME, 'epidemic_domestic_data', 'provinces')
    if not os.path.exists(city_json_file_directory):
        os.makedirs(city_json_file_directory)

    # TODO: 获取当天数据
    try:
        os.remove(input_file)
    except:
        pass
    url = 'https://github.com.cnpmjs.org/BlankerL/DXY-COVID-19-Data/releases/download/%s/DXYArea.csv' % datetime.strftime(datetime.today(), '%Y.%m.%d')
    download_from_url(url, input_file)

    f = open(input_file, "r", encoding='utf-8')
    title = f.readline()[:-1].split(',')
    all_data = []
    cities_in_province = {}
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
        single_data['updateTime'] = datetime.strptime(
            single_data['updateTime'].split(' ')[0].replace('/', '-'), '%Y-%m-%d')
        single_data['updateTime'] = datetime.strftime(
            single_data['updateTime'], '%Y-%m-%d')
        all_data.append(single_data)

        if single_data['provinceName'] not in cities_in_province.keys():
            cities_in_province[single_data['provinceName']] = []
        if single_data['cityName'] not in cities_in_province[single_data['provinceName']]:
            cities_in_province[single_data['provinceName']].append(single_data['cityName'])

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

    d = begin
    analysis = []
    idx = 0
    while all_data[idx]['updateTime'] != (d + delta).strftime('%Y-%m-%d'):
        idx += 1
    bar = tqdm(
        total=(end-begin).days + 1, initial=0, dynamic_ncols=True,
    )
    while d <= end:
        bar.update(1)
        bar.set_description('[extracting]')
        nd = d.strftime('%Y-%m-%d')
        bar.set_postfix_str(nd)
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

        while idx < len(all_data) and all_data[idx]['updateTime'] == (d + delta).strftime('%Y-%m-%d'):
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

        d += delta
    bar.close()

    # TODO: 在此更新最新一天的数据，数据源为akshare的丁香园接口，可以考虑写新importer更新当天最新数据
    # TODO: 发现akshare不行，丁香园就是不靠谱，考虑采用腾讯api
    # TODO: 现有最新数据7.8，今天7.10可以用akshare获取7.9数据，再使用腾讯api回去10号以及之后的最新数据

    # Build jsons
    city_back_to_front = {}
    for v, k in city_dict_ch.items():
        city_back_to_front[k] = v
    provinces = {}
    for p in province_dict_ch.values():
        provinces[p] = {}
    d = begin
    bar = tqdm(
        total=(end-begin).days + 1, initial=0, dynamic_ncols=True,
    )
    while d <= end:
        bar.set_description('[jsoning]')
        nd = d.strftime('%Y-%m-%d')
        bar.set_postfix_str(nd)
        daily_analysis = {'date': nd, 'provinces': []}
        for province_front, province in province_dict_ch.items():
            pd = {'name': province_front}
            provinces[province][nd] = []
            # TODO: 人口查询方式优化
            for it in province_population.items():
                if it[0] in province:
                    pd['population'] = it[1]
            data_new = {'died': daily_info[nd][province]['province_new_died'],
                        'cured': daily_info[nd][province]['province_new_cured'],
                        'confirmed': daily_info[nd][province]['province_new_confirmed']}
            data_total = {'died': daily_info[nd][province]['province_total_died'],
                          'cured': daily_info[nd][province]['province_total_cured'],
                          'confirmed': daily_info[nd][province]['province_total_confirmed']}
            pd['new'] = data_new
            pd['total'] = data_total
            daily_analysis['provinces'].append(pd)
            for city in cities_in_province[province]:
                if city in city_back_to_front.keys():
                    provinces[province][nd].append({
                        'name': city_back_to_front[city],
                        'new': {
                            'died': daily_info[nd][city]['city_new_died'],
                            'cured': daily_info[nd][city]['city_new_cured'],
                            'confirmed': daily_info[nd][city]['city_new_confirmed'],
                        },
                        'total': {
                            'died': daily_info[nd][city]['city_total_died'],
                            'cured': daily_info[nd][city]['city_total_cured'],
                            'confirmed': daily_info[nd][city]['city_total_confirmed'],
                        }
                    })

        analysis.append(daily_analysis)
        d += delta
    bar.close()
    
    json.dump(analysis, open(province_json_file, 'w'), ensure_ascii=False)
    for province_front, province in province_dict_ch.items():
        json.dump(provinces[province], open(os.path.join(city_json_file_directory, '%s.json' % province), 'w'),
                  ensure_ascii=False)


if __name__ == '__main__':
    epidemic_domestic_import()

