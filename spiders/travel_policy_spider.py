import json
import os
from tqdm import tqdm

from selenium import webdriver
import argparse
import xml
from xml.dom.minidom import parse
import xml.dom.minidom
import requests

from meta_config import SPIDER_DATA_DIRNAME


def get_input_options_by_json(path):
    res = {}
    if not os.path.exists(path):
        os.makedirs(path)
    with open(os.path.join(os.path.split(path)[0], 'travel_policy_cities.json'), 'r', encoding='utf-8') as jsonfile:
        js = json.load(jsonfile)
    for i in range(len(js['data'])):
        if js['data'][i]['province'] not in res.keys():
            res[js['data'][i]['province']] = []
        res[js['data'][i]['province']].append([js['data'][i]['city']])
    # with open(os.path.join(path, 'policy_by_city.json'), 'a', encoding='utf-8') as fp:
    #     fp.write(json.dumps(res) + '\n')
    return res


def spider(path, res):
    '''
    {"success":true,
    "code":0,
    "msg":"SUCCESS",
    "data":
    {"id":222,
    "province":"辽宁",
    "city":"朝阳","param1":    {"success":false,"code":2,"msg":"没有查询的城市","data":null}
    '''
    output_json_fname = os.path.join(path, 'policy_by_city.json')
    if os.path.exists(output_json_fname):
        os.remove(output_json_fname)
    
    url = 'http://wx.wind.com.cn/alert/traffic/getPolicy?city='

    bar = tqdm(range(len(list(res.keys()))), dynamic_ncols=True)
    for i in bar:
        bar.set_description(f'[line{i}]')
        city_list = res.get(list(res.keys())[i])
        for j in range(len(city_list)):
            get_url = url + city_list[j][0]
            response = requests.get(get_url, headers={'Content-Type': 'application/json'}, timeout=10)
            js = json.loads(response.text)
            if js['success']:
                with open(output_json_fname, 'a', encoding='utf-8') as fp:
                    fp.write(json.dumps({
                        'province': js['data']['province'],
                        'city': js['data']['city'],
                        'enter_policy': js['data']['enterPolicy'],
                        'out_policy': js['data']['outPolicy'],
                    }) + '\n')
    bar.close()


def main():
    parser = argparse.ArgumentParser(description='Train-Spider')
    parser.add_argument('--path', required=False, default=os.path.join(SPIDER_DATA_DIRNAME, 'travel_policy_spider_all'), type=str)
    args = parser.parse_args()
    res = get_input_options_by_json(args.path)
    print(res)
    spider(args.path, res)


if __name__ == '__main__':
    main()
