import datetime
import re
import json

import requests


def data_to_str(data: object):
    return json.dumps(data, ensure_ascii=False, indent=2, sort_keys=False)


def str_to_data(s: str):
    return json.loads(s) if s else None


def parse_datetime(datetime):
    return [int(x) for x in filter(lambda s: len(s) <= 4, re.split('[-:/ .]', str(datetime)))]


def cur_time():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def address_to_jingwei(address) -> (float, float):
    ret = gd_address_to_jingwei_and_province_city(address)
    if ret is None:
        return None, None
    else:
        return ret['jingdu'], ret['weidu']
    
    # todo: 下面的代码可以考虑全部删除了
    # 'showLocation&&showLocation({"status":0,"result":{"location":{"lng":116.38548789747735,"lat":39.871280236128878},"precise":0,"confidence":50,"comprehension":0,"level":"火车站"}})'
    # ak = '4PKHdx8ujI2T3R53ZvgC1ZOTWViHK8am'   # ？的
    # ak = '0wem7DQG7HjCVpzKk5y8y3kGnhPmMFRk'   # tky的
    # ak = 'vnRXRCTGp9RMnO6xbuGU497wta2P1FFj'   # wlt的
    ak = '11Z8uiP8kIz6AG0Vjiwzbc5f9Ii0cdHd'  # 网上找的
    url = 'http://api.map.baidu.com/geocoding/v3/?address=' + address + '&output=json&ak=' + ak \
          + '&callback=showLocation'
    try:
        res = requests.get(url=url)
    except:
        return None, None
    js_list = re.findall(r'showLocation&&showLocation\((.+)\)', res.text)
    if len(js_list):
        js = json.loads(js_list[0])
    else:
        print(res.text)
        return 0, 0
    if int(js['status']) == 0:
        jingdu = float(js['result']['location']['lng'])
        weidu = float(js['result']['location']['lat'])
    else:
        print(js['msg'], '地址：' + address)
        return 0, 0
    return jingdu, weidu


def gd_address_to_jingwei_and_province_city(address):
    '''
    return: res = {
        "jingdu": ,
        "weidu": ,
        "country": ,
        "province": ,
        "city": ,
        "district": ,
        "citycode": ,
    }
    '''
    # 推荐用高德！！比百度准好多！！查city还不用二次调用
    ak = '7275224ca913b751868e4076eb8212d5'
    url = 'https://restapi.amap.com/v3/geocode/geo?key=' + ak + '&address=' + address
    try:
        res = requests.get(url=url)
    except:
        return None
    js = json.loads(res.text)
    if 'geocodes' not in js.keys():
        print(f"address={address}: 无法获取所在城市（json.dumps(js)=\n{json.dumps(js, indent=2)}）")
        return None
    if not isinstance(js['geocodes'][0]['city'], str):
        print(f"address={address}: 无法获取所在城市（高德返回的js['geocodes'][0]['city']={js['geocodes'][0]['city']}）")
        return None
    if len(js['geocodes']) == 0:
        print(f"address={address}: 无法获取所在城市（高德返回的js['geocodes']={js['geocodes']}）")
        return None
    
    return {
        "jingdu": js['geocodes'][0]['location'].split(',')[0],
        "weidu": js['geocodes'][0]['location'].split(',')[1],
        "country": js['geocodes'][0]['country'],
        "province": js['geocodes'][0]['province'],
        "city": js['geocodes'][0]['city'],
        "district": js['geocodes'][0]['district'],
        "citycode": js['geocodes'][0]['citycode'] if 'citycode' in js['geocodes'][0].keys() else '',
    }

# todo：下面的代码已经无用，可以考虑删除
# def jingwei_to_address(jingdu, weidu):
#     '''
#     res = jingwei_to_address(jingdu, weidu)
#     查询省：res['result']['addressComponent']['province']
#     查询市：res['result']['addressComponent']['city']
#     查询区：res['result']['addressComponent']['district']
#     res是json：
# {
#   "status": 0,
#   "result": {
#     "location": {
#       "lng": 121.50989077799084,    # 经度
#       "lat": 31.22932842411674
#     },
#     "formatted_address": "上海市黄浦区中山南路187",
#     "business": "外滩,陆家嘴,董家渡",
#     "addressComponent": {
#       "country": "中国",
#       "country_code": 0,
#       "country_code_iso": "CHN",
#       "country_code_iso2": "CN",
#       "province": "上海市",
#       "city": "上海市",
#       "city_level": 2,
#       "district": "黄浦区",
#       "town": "",
#       "town_code": "",
#       "adcode": "310101",
#       "street": "中山南路",
#       "street_number": "187",
#       "direction": "东北",
#       "distance": "91"
#     },
#     "pois": [],
#     "roads": [],
#     "poiRegions": [],
#     "sematic_description": "",
#     "cityCode": 289
#   }
# }
#     '''
#     # ak = '4PKHdx8ujI2T3R53ZvgC1ZOTWViHK8am'   # ？的
#     # ak = '0wem7DQG7HjCVpzKk5y8y3kGnhPmMFRk'   # tky的
#     # ak = 'vnRXRCTGp9RMnO6xbuGU497wta2P1FFj'   # wlt的
#     ak = '11Z8uiP8kIz6AG0Vjiwzbc5f9Ii0cdHd'     # 网上找的
#     url = "http://api.map.baidu.com/reverse_geocoding/v3/?ak=" + ak \
#         +'&output=json&coordtype=wgs84ll&language=zh-CN&location=' + str(weidu) + ',' + str(jingdu)
#     try:
#         res = requests.get(url=url)
#     except:
#         return None, None
#     js = json.loads(res.text)
#     return js
