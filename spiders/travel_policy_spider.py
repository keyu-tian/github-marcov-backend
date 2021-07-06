import json
import os

from selenium import webdriver
import argparse
import xml
from xml.dom.minidom import parse
import xml.dom.minidom
import requests

# 城市的出行政策爬取

def get_input_options_by_xml(path):
    DOMTree = xml.dom.minidom.parse("./CountryProvinceCityLocListCH_and_Code.xml")
    china = DOMTree.documentElement.getElementsByTagName('CountryRegion').item(0).getElementsByTagName('State')
    res = {}
    for i in range(len(china)):
        state = china[i]
        city_list = state.getElementsByTagName('City')
        state_name = china[i].getAttribute('Name')
        res[state_name] = []
        for j in range(len(city_list)):
            city_name = city_list[j].getAttribute('Name')
            res[state_name].append(city_name)
    with open(os.path.join(path, 'policy_by_city.json'), 'a', encoding='utf-8') as fp:
        fp.write(json.dumps(res) + '\n')
    return res


def get_input_options_by_json(path):
    res = {}
    with open(os.path.join(path, 'City.json'), 'r', encoding='utf-8') as jsonfile:
        js = json.load(jsonfile)
    for i in range(len(js['data'])):
        if js['data'][i]['province'] not in res.keys():
            res[js['data'][i]['province']] = []
        res[js['data'][i]['province']].append([js['data'][i]['city']])
    # with open('./option_result.json', 'w+', encoding='utf-8') as jsonfile:
    if not os.path.exists(path):
        os.makedirs(path)
    with open(os.path.join(path, 'policy_by_city.json'), 'a', encoding='utf-8') as fp:
        fp.write(json.dumps(res) + '\n')
    return res


def main(path, res):
    '''
    {"success":true,
    "code":0,
    "msg":"SUCCESS",
    "data":
    {"id":222,
    "province":"辽宁",
    "city":"朝阳","param1":    {"success":false,"code":2,"msg":"没有查询的城市","data":null}
    '''
    url = 'http://wx.wind.com.cn/alert/traffic/getPolicy?city='
    for i in range(len(list(res.keys()))):
        city_list = res.get(list(res.keys())[i])
        for j in range(len(city_list)):
            get_url = url + city_list[j][0]
            response = requests.get(get_url, headers={'Content-Type': 'application/json'}, timeout=10)
            js = json.loads(response.text)
            if js['success']:
                with open(os.path.join(path, 'policy_by_city.json'), 'a', encoding='utf-8') as fp:
                    fp.write(json.dumps({
                        'province': js['data']['province'],
                        'city': js['data']['city'],
                        'enter_policy': js['data']['enterPolicy'],
                        'out_policy': js['data']['outPolicy'],
                    }) + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Train-Spider')
    parser.add_argument('--path', required=False, default=os.path.join('spiders_data', 'travel_policy_spider_all'), type=str)
    args = parser.parse_args()

    res = get_input_options_by_json(args.path)
    print(res)

    main(args.path, res)
