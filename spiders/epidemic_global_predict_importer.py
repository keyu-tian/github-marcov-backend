import json
import datetime
import os

from meta_config import SPIDER_DATA_DIRNAME
from spiders.epidemic_global_importer import dt_delta
from utils.country_dict import country_dict

PREDICT_TIME = 30  # 预测的天数
keys = ["confirmedCount.json", "curedCount.json", "deadCount.json"]

f1 = open(os.path.join("temp", "confirmedCount.json"), "r", encoding='utf-8')
f2 = open(os.path.join("temp", "curedCount.json"), "r", encoding='utf-8')
f3 = open(os.path.join("temp", "deadCount.json"), "r", encoding='utf-8')
datas_1 = json.load(f1)["data"]
datas_2 = json.load(f2)["data"]
datas_3 = json.load(f3)["data"]

dataout = []
begin = datetime.datetime.now().strftime("%Y-%m-%d")


def predict_global_import(start_dt=None):
    if start_dt is None:
        start_dt = begin
    while (datetime.datetime.strptime(start_dt, '%Y-%m-%d').date()
           - datetime.datetime.now().date()).days <= PREDICT_TIME:

        countries = []
        for (data_1, data_2, data_3) in zip(datas_1, datas_2, datas_3):
            country = data_1[0]
            if country not in country_dict.values():
                # print(country)
                # start_dt = dt_delta(start_dt, 1)
                continue
            date = datetime.datetime.strptime(data_1[1], "%Y%m%d").strftime('%Y-%m-%d')
            if date == start_dt:
                countries.append({
                    "name": country,
                    "population": 0,  # todo
                    "predict": {
                        "died": int(data_3[2]),
                        "cured": int(data_2[2]),
                        "confirmed": int(data_1[2]),
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
