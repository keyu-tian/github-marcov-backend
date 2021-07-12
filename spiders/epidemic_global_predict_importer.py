import json
import datetime
import math
import os

from meta_config import SPIDER_DATA_DIRNAME
from spiders.epidemic_global_importer import dt_delta
from utils.country_dict import country_dict
from tqdm import tqdm

PREDICT_TIME = 30  # 预测的天数
keys = ["confirmedCount.json", "curedCount.json", "deadCount.json"]

f1 = open(os.path.join(SPIDER_DATA_DIRNAME, "confirmedCount.json"), "r", encoding='utf-8')
f2 = open(os.path.join(SPIDER_DATA_DIRNAME, "curedCount.json"), "r", encoding='utf-8')
f3 = open(os.path.join(SPIDER_DATA_DIRNAME, "deadCount.json"), "r", encoding='utf-8')
datas_1 = json.load(f1)["data"]
datas_2 = json.load(f2)["data"]
datas_3 = json.load(f3)["data"]

dataout = []
begin = dt_delta(datetime.datetime.now().strftime("%Y-%m-%d"), -1)


def predict_global_import(start_dt=None):
    if start_dt is None:
        start_dt = begin
    yesterday = begin
    true_json = {}
    try:
        true_json = json.load(
            open(os.path.join(SPIDER_DATA_DIRNAME, "true_data.json"), "r", encoding='utf-8'))
    except FileNotFoundError:
        print("No true data!!")
    days = (datetime.datetime.now().date() - datetime.datetime.strptime(start_dt, '%Y-%m-%d').date()).days + 1
    bar = tqdm(
        total=days, initial=0, dynamic_ncols=True,
    )
    # last_confirmed = {}
    # last_cured = {}
    # last_died = {}
    a1, a2, a3 = 0.0, 0.0, 0.0
    while (datetime.datetime.strptime(start_dt, '%Y-%m-%d').date()
           - datetime.datetime.now().date()).days <= PREDICT_TIME:
        bar.set_description('[parsing]')
        bar.update(1)
        bar.set_postfix_str(start_dt)
        countries = []
        alpha = {}
        for (data_1, data_2, data_3) in zip(datas_1, datas_2, datas_3):
            country = data_1[0]
            if country not in country_dict.values() or country not in true_json.keys():
                continue
            date = datetime.datetime.strptime(data_1[1], "%Y%m%d").strftime('%Y-%m-%d')
            # print(country)
            # data_1[4] data_2[4] data_3[4]
            # x = data_1[4] if data_1[4] is not None else data_1[3]  # y_max
            # y = data_2[4] if data_2[4] is not None else data_2[3]  # y_max
            # z = data_3[4] if data_3[4] is not None else data_3[3]  # y_max
            if date == yesterday:
                # if math.fabs(true_json[country]["confirmed"] - data_1[2]) > 1000:
                # a1 = (true_json[country]["confirmed"] - data_1[3]) / (x - data_1[3] + 1e-8)
                # a2 = (true_json[country]["cured"] - data_2[3]) / (y - data_2[3] + 1e-8)
                # a3 = (true_json[country]["died"] - data_3[3]) / (z - data_3[3] + 1e-8)
                # alpha[country] = [a1, a2, a3]
                # last_confirmed[country] = int(alpha[country][0] * x + (1 - alpha[country][0]) * data_1[3])
                # last_cured[country] = int(alpha[country][1] * y + (1 - alpha[country][1]) * data_2[3])
                # last_died[country] = int(alpha[country][2] * z + (1 - alpha[country][2]) * data_3[3])
                a1 = true_json[country]["confirmed"] / data_1[2] if data_1[2] != 0 else 0.0
                a2 = true_json[country]["cured"] / data_2[2] if data_2[2] != 0 else 0.0
                a3 = true_json[country]["died"] / data_3[2] if data_3[2] != 0 else 0.0

            # print(last_confirmed)
            if date == start_dt:
                # print(country)
                # confirmed = int(alpha[country][0] * x + (1 - alpha[country][0]) * data_1[3])
                # cured = int(alpha[country][1] * y + (1 - alpha[country][1]) * data_2[3])
                # died = int(alpha[country][2] * z + (1 - alpha[country][2]) * data_3[3])
                # if confirmed / (last_confirmed.get(country) + 1e-8) > 1.2:
                #     confirmed = last_confirmed.get(country) + 1 if last_confirmed.get(country) > 0 else 0
                # if cured / (last_cured.get(country) + 1e-8) > 1.1:
                #     cured = last_cured.get(country) + 1 if last_cured.get(country) > 0 else 0
                # if died / (last_died.get(country) + 1e-8) > 1.1:
                #     died = last_died.get(country) + 1 if last_died.get(country) > 0 else 0
                # last_confirmed[country] = confirmed
                # last_died[country] = died
                # last_cured[country] = cured
                countries.append({
                    "name": country,
                    "population": 0,  # todo
                    "predict": {
                        "confirmed": int(a1 * data_1[2]),
                        "cured": int(a2 * data_2[2]) if int(a2 * data_2[2]) < int(a1 * data_1[2]) else int(a1 * data_1[2]),
                        "died": int(a3 * data_3[2]),
                    }
                })
        dataout.append({
            "date": start_dt,
            "countries": countries
        })
        start_dt = dt_delta(start_dt, 1)

    with open(os.path.join(SPIDER_DATA_DIRNAME, 'predict.json'), 'w', encoding='utf-8') as f:
        json.dump(dataout, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    predict_global_import()
    print("Done!!!")
