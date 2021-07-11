import json
import os
import re
# import marcov19.settings
# from django.conf import settings
#
# from utils.dict_ch import city_dict_ch
#
# settings.configure(DEBUG=True, default_settings=marcov19.settings)
# import os
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marcov19.settings')
# import django
#
# django.setup()
from tqdm import tqdm

from country.models import City
from meta_config import SPIDER_DATA_DIRNAME, BULK_CREATE_BATCH_SIZE
from train.models import Train, Station, MidStation
from utils.cast import gd_address_to_jingwei_and_province_city

day_ch = ['第未知天', '第一天', '第二天', '第三天', '第四天', '第五天', '第六天', '第七天', '第八天', '第九天', '第十天', '终到站']


def cmp(item):
    _, mid_sta_name, day, st_t, ed_t, dt, dist, _, _, _ = item['content']
    if st_t == '起点站':
        return '000'
    if ed_t == '终到站':
        return '999'
    return f'{day_ch.index(day):03d}' + st_t


def train_import(line_start=0):
    Station.objects.all().delete()
    MidStation.objects.all().delete()
    Train.objects.all().delete()

    with open(os.path.join(SPIDER_DATA_DIRNAME, 'train_spider_all', '火车班次json数据_xc.json'), 'r',
              encoding='utf-8') as file:
        bar = tqdm(list(enumerate(file.readlines())), dynamic_ncols=True)
    __train_import(bar, line_start, 1)

    with open(os.path.join(SPIDER_DATA_DIRNAME, 'train_spider_all', '火车班次json数据.json'), 'r',
              encoding='utf-8') as file:
        bar = tqdm(list(enumerate(file.readlines())), dynamic_ncols=True)
    __train_import(bar, line_start, 2)



def __train_import(bar, line_start=0, src=1):
    # objs = []
    for line, result in bar:
        bar.set_description(f'[line{line}]')
        if line < line_start:
            continue
        try:
            result = json.loads(result)
        except:
            result = None
        if result:
            name = list(result.get('trainInfo').keys())[0]
            dept_sta_name = result.get('trainInfo').get(name).get('deptStation')
            dept_time = result.get('trainInfo').get(name).get('deptTime')
            dept_date = result.get('trainInfo').get(name).get('dptDate')
            arri_sta_name = result.get('trainInfo').get(name).get('arriStation')
            arri_time = result.get('trainInfo').get(name).get('arriTime')
            arri_date = result.get('trainInfo').get(name).get('arrDate')

            bar.set_postfix_str(f'{dept_sta_name} => {arri_sta_name}')

            dept_sta, flag = Station.objects.get_or_create(name_ch=dept_sta_name)
            if flag:  # 数据库没有的新的火车站，存经纬度
                res = gd_address_to_jingwei_and_province_city(dept_sta_name + '站')
                if res is None:
                    dept_sta.jingdu, dept_sta.weidu = 0, 0
                    res = gd_address_to_jingwei_and_province_city(dept_sta_name)
                    if res is None:
                        dept_sta.jingdu, dept_sta.weidu = 0, 0
                        city_name = "未知"
                        province_name = "未知"
                    else:
                        dept_sta.jingdu, dept_sta.weidu = res['jingdu'], res['weidu']
                        city_name = res['city']
                        province_name = res['province']
                else:
                    dept_sta.jingdu, dept_sta.weidu = res['jingdu'], res['weidu']
                    city_name = res['city']
                    province_name = res['province']
                dept_city_name_standar = City.standardize_name(city_name)
                if dept_city_name_standar is not None:
                    city_name = dept_city_name_standar
                dept_sta.city_name = city_name
                dept_sta.province_name = province_name
                dept_sta.save()

            arri_sta, flag = Station.objects.get_or_create(name_ch=arri_sta_name)
            if flag:  # 数据库没有的新的火车站，存经纬度
                res = gd_address_to_jingwei_and_province_city(arri_sta_name + '站')
                if res is None:
                    arri_sta.jingdu, arri_sta.weidu = 0, 0
                    res = gd_address_to_jingwei_and_province_city(arri_sta_name)
                    if res is None:
                        arri_sta.jingdu, arri_sta.weidu = 0, 0
                        city_name = "未知"
                        province_name = "未知"
                    else:
                        arri_sta.jingdu, arri_sta.weidu = res['jingdu'], res['weidu']
                        city_name = res['city']
                        province_name = res['province']
                else:
                    arri_sta.jingdu, arri_sta.weidu = res['jingdu'], res['weidu']
                    city_name = res['city']
                    province_name = res['province']
                arri_city_name_standar = City.standardize_name(city_name)
                if arri_city_name_standar is not None:
                    city_name = arri_city_name_standar
                arri_sta.city_name = city_name
                arri_sta.province_name = province_name
                arri_sta.save()
            train, flag = Train.objects.get_or_create(name=name, defaults={'dept_date': dept_date,
                                                                           'dept_time': dept_time,
                                                                           'arri_date': arri_date,
                                                                           'arri_time': arri_time})
            if flag:
                train.dept_station = dept_sta
                train.arri_station = arri_sta
                # train.dept_city_name = dept_city_name
                # train.arri_city_name = arri_city_name
                train.interval = result.get('extInfo').get('allTime')
                train.kilometer = result.get('extInfo').get('allMileage')
                mid_list = result.get('trainScheduleBody')
                if src == 2:
                    # 去哪儿网的数据要排序，携程的不用
                    mid_list.sort(key=lambda ci: float(str(ci['content'][-4]).strip('公里').strip()))
                for c in mid_list:
                    content = c.get('content')
                    sta, flag = Station.objects.get_or_create(name_ch=content[1])
                    if flag:  # 是新建，存经纬度
                        res = gd_address_to_jingwei_and_province_city(content[1] + '站')
                        if res is None:
                            sta.jingdu, sta.weidu = 0, 0
                            res = gd_address_to_jingwei_and_province_city(content[1])
                            if res is None:
                                sta.jingdu, sta.weidu = 0, 0
                                city_name = "未知"
                                province_name = "未知"
                            else:
                                sta.jingdu, sta.weidu = res['jingdu'], res['weidu']
                                city_name = res['city']
                                province_name = res['province']
                        else:
                            sta.jingdu, sta.weidu = res['jingdu'], res['weidu']
                            city_name = res['city']
                            province_name = res['province']

                        mid_city_name_standar = City.standardize_name(city_name)
                        if mid_city_name_standar is not None:
                            city_name = mid_city_name_standar
                        sta.province_name = province_name
                        sta.city_name = city_name
                        sta.save()
                    if src == 1:
                        index = int(content[2])
                    else:
                        index = mid_list.index(c) + 1
                    MidStation.objects.create(index=index, arri_date='',
                        arri_time=content[3], station=sta, train=train)
                    # objs.append(MidStation(
                    #     index=int(content[2]), arri_date='',
                    #     arri_time=content[3], station=sta, train=train
                    # ))
                train.save()
            else:
                with open(os.path.join(SPIDER_DATA_DIRNAME, 'train_spider_all', 'train_data_double_in_xc_qn.json'), 'a', encoding='utf-8') as file:
                    file.write(name + '\n')
        else:
            bar.set_postfix_str(f'failed!')
    # MidStation.objects.bulk_create(objs, batch_size=BULK_CREATE_BATCH_SIZE)


if __name__ == '__main__':
    train_import()