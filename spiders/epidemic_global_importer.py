import datetime
import time
import os

import pandas
from tqdm import tqdm

from epidemic.models import HistoryEpidemicData
from meta_config import IMPORTER_DATA_DIRNAME
from utils.country_dict import country_dict
import json

years = [2020, 2021]
months = [x for x in range(1, 13)]
days = [30, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

path = os.path.join(IMPORTER_DATA_DIRNAME, 'COVID-19', 'csse_covid_19_data', 'csse_covid_19_daily_reports')

# date	yyyy-mm-dd
begin = '2020-03-23'


def dt_change_ymd(date):
    # 月-日-年 -> 年-月-日
    return datetime.datetime.strftime(datetime.datetime.strptime(date, "%m-%d-%Y"), "%Y-%m-%d")


def dt_change_mdy(date):
    # 年-月-日 -> 月-日-年
    return datetime.datetime.strftime(datetime.datetime.strptime(date, "%Y-%m-%d"), "%m-%d-%Y")


def dt_delta(date, delta):
    dt = datetime.datetime.strptime(date, "%Y-%m-%d") + datetime.timedelta(days=delta)
    return dt.strftime('%Y-%m-%d')


# def time_cmp(first_time, second_time):
#     return int(time.strftime("%Y%m%d", first_time)) - int(time.strftime("%Y%m%d", second_time))


def epidemic_global_import(start_dt):
    dataout = []
    while start_dt < datetime.datetime.now().strftime("%Y-%m-%d"):
        t = time.time()
        print(start_dt)
        daily_data = {'date': start_dt}
        countries = {}
        try:
            file_name = dt_change_mdy(start_dt)
            last_file_name = dt_change_mdy(dt_delta(start_dt, -1))
            last_data = pandas.read_csv(path + last_file_name + '.csv').fillna(0)
            data = pandas.read_csv(path + file_name + '.csv').fillna(0)
            last_data = pandas.read_csv(os.path.join(path, last_file_name + '.csv')).fillna(0)
            data = pandas.read_csv(os.path.join(path, file_name + '.csv')).fillna(0)

            objs = []
            # data =data.dropna()
            bar = tqdm(list(zip(data.iterrows(), last_data.iterrows())))
            bar.set_description(start_dt)

            for (index, row), (last_index, last_row) in bar:
                # if row['Country_Region'] == 'China':
                #    continue
                objs.append(HistoryEpidemicData(**{
                    'date': start_dt, 'country_ch': row['Country_Region'],
                    'state_en': row['Province_State'],
                    'province_total_confirmed': row['Confirmed'],
                    'province_total_cured': row['Recovered'],
                    'province_total_died': row['Deaths'],
                    'province_new_died': max(row['Deaths'] - last_row['Deaths'], 0),
                    'province_new_cured': max(row['Recovered'] - last_row['Recovered'], 0),
                    'province_new_confirmed': max(row['Confirmed'] - last_row['Confirmed'], 0)
                }))
                if row['Country_Region'] not in country_dict.keys():
                    continue
                if row['Country_Region'] not in countries.keys():
                    countries[row['Country_Region']] = {
                        'name': country_dict[row['Country_Region']],
                        'population': 0, # todo: population
                        'new': {
                            'died': 0,
                            'cured': 0,
                            'confirmed': 0
                        },
                        'total': {
                            'died': 0,
                            'cured': 0,
                            'confirmed': 0
                        }
                    }
                countries[row['Country_Region']]['new']['died'] += max(row['Deaths'] - last_row['Deaths'], 0)
                countries[row['Country_Region']]['new']['cured'] += max(row['Recovered'] - last_row['Recovered'], 0)
                countries[row['Country_Region']]['new']['confirmed'] += max(row['Confirmed'] - last_row['Confirmed'], 0)
                countries[row['Country_Region']]['total']['died'] += row['Deaths']
                countries[row['Country_Region']]['total']['cured'] += row['Recovered']
                countries[row['Country_Region']]['total']['confirmed'] += row['Confirmed']


            HistoryEpidemicData.objects.bulk_create(objs)
            print(time.time() - t)
        except FileNotFoundError:
            print('File not found %s' % file_name)
            start_dt = dt_delta(start_dt, 1)
            continue
        except Exception as e:
            raise e
        daily_data['countries'] = list(countries.values())
        dataout.append(daily_data)
        start_dt = dt_delta(start_dt, 1)
    json.dump(dataout, open('global.json', 'w'), ensure_ascii=False)
