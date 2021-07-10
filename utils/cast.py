import datetime
import re
import json
import base64
import urllib

import requests

#
# def encode(s):
#     return urllib.parse.quote(base64.b64encode(str(s).encode()).decode(encoding="utf-8"))
#     # return str(s)
#
#
# def decode(s):
#     if isinstance(s, bytes):
#         s = s.decode()
#     s = urllib.parse.unquote(s)
#     return base64.b64decode(s).decode(encoding="utf-8")
#     # return s


def data_to_str(data: object):
    return json.dumps(data, ensure_ascii=False, indent=2, sort_keys=False)


def str_to_data(s: str):
    return json.loads(s) if s else None


def parse_datetime(datetime):
    return [int(x) for x in filter(lambda s: len(s) <= 4, re.split('[-:/ .]', str(datetime)))]


def cur_time():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def address_to_jingwei(address) -> (float, float):
    # 'showLocation&&showLocation({"status":0,"result":{"location":{"lng":116.38548789747735,"lat":39.871280236128878},"precise":0,"confidence":50,"comprehension":0,"level":"火车站"}})'
    ak = '4PKHdx8ujI2T3R53ZvgC1ZOTWViHK8am'
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


def jingwei_to_address(jingdu, weidu):
    '''
    res = jingwei_to_address(jingdu, weidu)
    查询省：res['result']['addressComponent']['province']
    查询市：res['result']['addressComponent']['city']
    查询区：res['result']['addressComponent']['district']
    res是json：
{
  "status": 0,
  "result": {
    "location": {
      "lng": 121.50989077799084,    # 经度
      "lat": 31.22932842411674
    },
    "formatted_address": "上海市黄浦区中山南路187",
    "business": "外滩,陆家嘴,董家渡",
    "addressComponent": {
      "country": "中国",
      "country_code": 0,
      "country_code_iso": "CHN",
      "country_code_iso2": "CN",
      "province": "上海市",
      "city": "上海市",
      "city_level": 2,
      "district": "黄浦区",
      "town": "",
      "town_code": "",
      "adcode": "310101",
      "street": "中山南路",
      "street_number": "187",
      "direction": "东北",
      "distance": "91"
    },
    "pois": [],
    "roads": [],
    "poiRegions": [],
    "sematic_description": "",
    "cityCode": 289
  }
}
    '''
    ak = "vnRXRCTGp9RMnO6xbuGU497wta2P1FFj"
    url = "http://api.map.baidu.com/reverse_geocoding/v3/?ak=" + ak \
        +'&output=json&coordtype=wgs84ll&language=zh-CN&location=' + str(weidu) + ',' + str(jingdu)
    try:
        res = requests.get(url=url)
    except:
        return None, None
    js = json.loads(res.text)
    return js
