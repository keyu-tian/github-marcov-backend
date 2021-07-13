import datetime
import json
import os

import pandas
import requests
from retrying import retry
from tqdm import tqdm

from meta_config import SPIDER_DATA_DIRNAME
from spiders.epidemic_China_total_importer import epidemic_China_total_import
from utils.country_dict import country_dict, re_country_vaacinations_dict
from utils.download import download_from_url


def dt_change_ymd(date):
    # 月-日-年 -> 年-月-日
    return datetime.datetime.strftime(datetime.datetime.strptime(date, "%m-%d-%Y"), "%Y-%m-%d")


def dt_change_mdy(date):
    # 年-月-日 -> 月-日-年
    return datetime.datetime.strftime(datetime.datetime.strptime(date, "%Y-%m-%d"), "%m-%d-%Y")


def dt_delta(date, delta):
    dt = datetime.datetime.strptime(date, "%Y-%m-%d") + datetime.timedelta(days=delta)
    return dt.strftime('%Y-%m-%d')


def dt_change_slash(date, s):  # yyyy(s)mm(s)dd -> yyyy/mm/dd
    return datetime.datetime.strptime(date, "%Y" + s + "%m" + s + "%d").strftime('%Y/%m/%d')


def dt_change_line(date, s):  # yyyy(s)mm(s)dd -> yyyy-mm-dd
    return datetime.datetime.strptime(date, "%Y" + s + "%m" + s + "%d").strftime('%Y-%m-%d')


# 返回 date1 与 date2 相差天数
def dt_cmp(d1, d2) -> int:
    return (datetime.datetime.strptime(d1, "%Y-%m-%d") - datetime.datetime.strptime(d2, "%Y-%m-%d")).days


url = 'https://api.inews.qq.com/newsqa/v1/automation/foreign/daily/list?country='
url_world = "https://api.inews.qq.com/newsqa/v1/automation/modules/list?modules=FAutoGlobalStatis"
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 '
                  'Safari/537.36 Core/1.70.3741.400 QQBrowser/10.5.3863.400 '
}

begin = '2020-02-01'

dataout = []


@retry(stop_max_attempt_number=10, wait_random_min=100, wait_random_max=2000)
def requests_get(url, headers):
    res = requests.get(url, headers=headers, verify=False)
    return json.loads(res.text)['data']


def epidemic_global_import(start_dt=None):
    vacc_file = os.path.join(SPIDER_DATA_DIRNAME, 'vaccinations.csv')
    if os.path.exists(vacc_file):
        os.remove(vacc_file)
    download_from_url('https://github.com.cnpmjs.org/owid/covid-19-data/raw/master/public/data/vaccinations/vaccinations.csv', vacc_file)
    data_vaccinations = pandas.read_csv(vacc_file).fillna(0)

    requests.packages.urllib3.disable_warnings()
    if start_dt is None:
        start_dt = begin
    tmp = []  # [{'date':'2020-03-22', 'country_info':{}}, {...}, ...]
    bar = tqdm(list(country_dict.values()))
    # bar.set_description(start_dt)
    for country in bar:
        if country == "日本":
            response_data = requests_get(url + "日本本土", headers=headers)
        elif country == "印度尼西亚, 印尼":
            response_data = requests_get(url + "印度尼西亚", headers=headers)
        elif country == "刚果":
            response_data = requests_get(url + "刚果（布）", headers=headers)
        elif country == "刚果民主共和国":
            response_data = requests_get(url + "刚果（金）", headers=headers)
        elif country == "中非":
            response_data = requests_get(url + "中非共和国", headers=headers)
        elif country == "孟加拉国":
            response_data = requests_get(url + "孟加拉", headers=headers)
        elif country == "波斯尼亚和黑塞哥维那":
            response_data = requests_get(url + "波黑", headers=headers)
        elif country == "多米尼加共和国":
            response_data = requests_get(url + "多米尼加", headers=headers)
        elif country == "马其顿":
            response_data = requests_get(url + "北马其顿", headers=headers)
        elif country == "列支敦士登":
            response_data = requests_get(url + "列支敦士登公国", headers=headers)
        else:
            response_data = requests_get(url + country, headers=headers)
        if response_data is None and country != "中国":
            print(f'[None] {country}')
        elif country == "中国":
            date = start_dt
            last_total_vaccinated = 0
            while date <= datetime.datetime.now().strftime("%Y-%m-%d"):
                data_vacc = data_vaccinations[(data_vaccinations['date'] == date) &
                                              ((data_vaccinations['location'] == 'China') |
                                               (data_vaccinations['location'] == 'Hong Kong') |
                                               (data_vaccinations['location'] == 'Taiwan') |
                                               (data_vaccinations['location'] == 'Macao'))]
                if (datetime.datetime.now().date() - datetime.datetime.strptime(date, '%Y-%m-%d').date()).days <= 2:
                    total_vaccinated = last_total_vaccinated
                elif data_vacc.empty:
                    new_vaccinated = "未知"
                    total_vaccinated = "未知"
                else:
                    new_vaccinated = \
                        int(sum(data_vacc["daily_vaccinations"])) if int(
                            sum(data_vacc["daily_vaccinations"])) != 0 else "未知"
                    total_vaccinated = int(sum(data_vacc["total_vaccinations"]))
                    if total_vaccinated == 0:
                        total_vaccinated = \
                            last_total_vaccinated + new_vaccinated if new_vaccinated != "未知" else total_vaccinated
                    last_total_vaccinated = total_vaccinated
                China_info = epidemic_China_total_import(date)
                if China_info is None and date != datetime.datetime.now().strftime("%Y-%m-%d"):
                    date = dt_delta(date, 1)
                    continue
                elif China_info is None and date == datetime.datetime.now().strftime("%Y-%m-%d"):
                    China_info = epidemic_China_total_import(dt_delta(date, -1))
                country_info = {
                    "name": country,
                    "population": 0,  # todo
                    "new": China_info["new"],
                    "total": China_info["total"]
                }
                country_info["new"]["vaccinated"] = new_vaccinated
                country_info["total"]["vaccinated"] = total_vaccinated
                tmp.append({"date": date, "country_info": country_info})
                date = dt_delta(date, 1)
        else:
            # 对于指定国家，遍历每个日期
            last_total_vaccinated = 0
            for (index, i) in enumerate(list(response_data)):
                date = dt_change_line(i["y"] + "." + i["date"], s=".")  # yyyy-mm-dd
                # 获取疫苗接种情况
                country_vacc = re_country_vaacinations_dict.get(country)
                data_vacc = data_vaccinations[(data_vaccinations['date'] == date) &
                                              (data_vaccinations['location'] == country_vacc)]
                if (datetime.datetime.now().date() - datetime.datetime.strptime(date, '%Y-%m-%d').date()).days <= 2:
                    total_vaccinated = last_total_vaccinated
                elif data_vacc.empty:
                    new_vaccinated = "未知"
                    total_vaccinated = "未知"
                else:
                    new_vaccinated = \
                        int(sum(data_vacc["daily_vaccinations"])) if int(
                            sum(data_vacc["daily_vaccinations"])) != 0 else "未知"
                    total_vaccinated = int(sum(data_vacc["total_vaccinations"]))
                    if total_vaccinated == 0:
                        total_vaccinated = \
                            last_total_vaccinated + new_vaccinated if new_vaccinated != "未知" else total_vaccinated
                    last_total_vaccinated = total_vaccinated
                country_info = {
                    "name": country,
                    "population": 0,  # todo
                    "new": {
                        "died": 0 if index == 0 else max(i["dead"] - response_data[index - 1]["dead"], 0),
                        "cured": 0 if index == 0 else max(i["heal"] - response_data[index - 1]["heal"], 0),
                        "confirmed": i['confirm_add'],
                        "vaccinated": new_vaccinated
                    },
                    "total": {
                        "died": i["dead"],
                        "cured": i["heal"],
                        "confirmed": i["confirm"],
                        "vaccinated": total_vaccinated
                    }}
                tmp.append({"date": date, "country_info": country_info})

    # 遍历每个时间直到当前
    days = (datetime.datetime.now().date() - datetime.datetime.strptime(start_dt, '%Y-%m-%d').date()).days + 1
    bar = tqdm(
        total=days, initial=0, dynamic_ncols=True,
    )

    true_data = {}
    today_data = {}
    while start_dt <= datetime.datetime.now().strftime("%Y-%m-%d"):
        bar.set_description('[parsing]')
        bar.update(1)
        bar.set_postfix_str(start_dt)
        countries = []
        for i in tmp:
            if i["date"] == start_dt:
                countries.append(i["country_info"])
                # 做一个真实数据，为预测做准备
                if start_dt == dt_delta(datetime.datetime.now().strftime("%Y-%m-%d"), -1):
                    true_data[i["country_info"]["name"]] = i["country_info"]["total"]
                    true_data[i["country_info"]["name"]]["new_confirmed"] = i["country_info"]["new"]["confirmed"]
                    true_data[i["country_info"]["name"]]["new_cured"] = i["country_info"]["new"]["cured"]
                    true_data[i["country_info"]["name"]]["new_died"] = i["country_info"]["new"]["died"]

        dataout.append({
            "date": start_dt,
            "countries": countries
        })
        start_dt = dt_delta(start_dt, 1)
    bar.close()

    response_data = requests_get(url_world, headers=headers)["FAutoGlobalStatis"]
    # "nowConfirm":27722322,"confirm":186625242,"heal":154877929,"dead":4024991,"nowConfirmAdd":67126,
    # "confirmAdd":265520,"healAdd":194268,"deadAdd":4126,"lastUpdateTime":"2021-07-10 10:22:42"}}}
    today = {
        "update": response_data["lastUpdateTime"],
        'new': {
            "died": response_data["deadAdd"],
            "cured": response_data["healAdd"],
            "confirmed": response_data["confirmAdd"],
        },
        'total': {
            "died": response_data["dead"],
            "cured": response_data["heal"],
            "confirmed": response_data["confirm"],
        }
    }
    dataout.append(today)

    with open(os.path.join(SPIDER_DATA_DIRNAME, 'global.json'), 'w', encoding='utf-8') as f:
        json.dump(dataout, f, ensure_ascii=False, indent=2)

    with open(os.path.join(SPIDER_DATA_DIRNAME, 'true_data.json'), 'w', encoding='utf-8') as f:
        json.dump(true_data, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    epidemic_global_import()
