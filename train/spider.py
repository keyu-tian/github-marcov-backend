import argparse
import datetime
import json
import requests
import sys
import time
import marcov19.settings
from django.conf import settings
from utils.log import create_logger


settings.configure(DEBUG=True, default_settings=marcov19.settings)
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marcov19.settings')
import django
django.setup()


from country.models import Country, City
from train.models import Train, Station, MidStation

# 暂时不管Gxxx/Gxxx格式的版本
from requests.exceptions import Timeout
from utils.cast import address_to_jingwei

URL = 'http://train.qunar.com/qunar/checiInfo.jsp'
DEFAULT_DATE = datetime.datetime.now()
DEFAULT_DATE_STR = DEFAULT_DATE.strftime('%Y-%m-%d')  # 默认查询当天的

mingming = [('G', 9999),
            ('C', 9999),
            ('Z', 9999),
            ('T', 9999),
            ('K', 9999),
            ('L', 9999),
            ('Y', 999)]


def getinfo(logger, train_number='G99', date=DEFAULT_DATE_STR):
    logger.info('getinfo')
    params = {
        'method_name': 'buy',
        'ex_track': '',
        'q': train_number,
        'date': date.replace('-', ''),
        'format': 'json',
        'cityname': 123456,
        'ver': int(time.time() * 1000),
    }
    url = URL
    try:
        response = requests.get(url=url, params=params, headers={'Content-Type': 'application/json'}, timeout=10)
    except Timeout:
        logger.error('无法从服务器获取数据')
        logger.error('url: ' + url)
        logger.error(params)
        return None
    result = json.loads(response.text)
    if result == {'count': 0}:
        logger.error('无法获取该火车班次，班次为' + train_number)
        return None
    return result


def main(path, index=0, st=1):
    if not os.path.exists(path):
        os.makedirs(path)

    logger = create_logger(logger_name='spider', log_path=os.path.join(path, 'spider.log'), to_stdout=False)

    country, flag = Country.objects.get_or_create(name_ch='中国', defaults={'name_en': 'Chinese'})
    for a in range(index, len(mingming)):
        for i in range(st, mingming[a][1]):
            if 0 <= datetime.datetime.now().hour <= 6:
                time.sleep(1)
            else:
                time.sleep(3)
            name = mingming[a][0] + str(i)
            result = getinfo(logger=logger, train_number=name)  # result是json
            if result and not Train.objects.filter(name=name).exists():
                dept_city_name = result.get('trainInfo').get(name).get('deptCity')
                dept_sta_name = result.get('trainInfo').get(name).get('deptStation')
                dept_time = result.get('trainInfo').get(name).get('deptTime')
                dept_date = result.get('trainInfo').get(name).get('deptTime')
                arri_city_name = result.get('trainInfo').get(name).get('deptCity')
                arri_sta_name = result.get('trainInfo').get(name).get('deptStation')
                arri_time = result.get('trainInfo').get(name).get('deptTime')
                arri_date = result.get('trainInfo').get(name).get('deptTime')

                dept_city, flag = City.objects.get_or_create(name_ch=dept_city_name)
                if flag:  # 数据库没有的新的国家，存名字
                    dept_city.country = country
                    dept_city.save()
                dept_sta, flag = Station.objects.get_or_create(name_cn=dept_sta_name)
                if flag:  # 数据库没有的新的火车站，存经纬度
                    dept_sta.jingdu, dept_sta.weidu = address_to_jingwei(dept_sta_name + '站')
                    dept_sta.city = dept_city
                    dept_sta.save()

                arri_city, flag = City.objects.get_or_create(name_ch=arri_city_name)
                if flag:  # 数据库没有的新的国家，存名字
                    arri_city.country = country
                    arri_city.save()
                arri_sta, flag = Station.objects.get_or_create(name_cn=arri_sta_name)
                if flag:  # 数据库没有的新的火车站，存经纬度
                    arri_sta.jingdu, arri_sta.weidu = address_to_jingwei(arri_sta_name + '站')
                    arri_sta.city = arri_city
                    arri_sta.save()
                train, flag = Train.objects.get_or_create(name=name, defaults={'dept_date': dept_date,
                                                                         'dept_time': dept_time,
                                                                         'arri_date': arri_date,
                                                                         'arri_time': arri_time})
                if flag:
                    mid_list = result.get('trainScheduleBody')
                    for c in mid_list:
                        content = c.get('content')
                        sta, flag = Station.objects.get_or_create(name_cn=content[1])
                        if flag:  # 是新建，存经纬度
                            sta.jingdu, sta.weidu = address_to_jingwei(arri_sta_name + '站')
                            sta.city = arri_city
                            sta.save()
                        MidStation.objects.create(index=mid_list.index(c) + 1, arri_date=content[2],
                                                  arri_time=content[3], station=sta, train=train)
                train.interval = result.get('extInfo').get('allTime')
                train.kilometer = result.get('extInfo').get('allMileage')
                train.save()
                with open(os.path.join(path, '火车班次json数据.json'), 'a', encoding='utf-8') as fp:
                    fp.write(str(result) + '\n')
                with open(os.path.join(path, '火车班次列表.json'), 'a', encoding='utf-8') as fp:
                    fp.write(name + '\n')



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Train-Spider')
    parser.add_argument('--path', required=False, default='train_crawler', type=str)
    parser.add_argument('--index', required=False, default=0, type=int)
    parser.add_argument('--st', required=False, default=1, type=int)
    args = parser.parse_args()

    start = str(datetime.datetime.now())
    print(f'[{start}] 开始爬取，path={args.path}, index={args.index}, st={args.st}...')
    main(args.path, args.index, args.st)
    end = str(datetime.datetime.now())
    print(f'抓取完毕，请进入{args.path}文件夹查看数据，进入spider.log文件夹查看日志；开始时间为' + start + '结束时间为' + end)

    # res = getinfo('G1317')
    # print(res)

    # url = 'http://train.qunar.com/qunar/checiSuggest.jsp?callback=jQuery17208000492092391186_1460000280989&include_coach_suggest=true&lang=zh&q=G1316&sa=true&format=js&_=1460000429009'
    # try:
    #     response = requests.get(url=url, timeout=10)
    # except Timeout:
    #     logger.error('无法从服务器获取数据')
    #     logger.error('url: '+url)
    # results=json.loads('{'+response.text.split('({')[1].split('})')[0]+'}')['result']
    # print(results[0].get('key'))
