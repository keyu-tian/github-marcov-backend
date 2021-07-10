import json
import os

from tqdm import tqdm

from country.models import City
from meta_config import SPIDER_DATA_DIRNAME, BULK_CREATE_BATCH_SIZE
from train.models import Train, Station, MidStation

day_ch = ['第未知天', '第一天', '第二天', '第三天', '第四天', '第五天', '第六天', '第七天', '第八天', '第九天', '第十天', '终到站']


def cmp(item):
    _, mid_sta_name, day, st_t, ed_t, dt, dist, _, _, _ = item['content']
    if st_t == '起点站':
        return '000'
    if ed_t == '终到站':
        return '999'
    return f'{day_ch.index(day):03d}' + st_t


def train_import(line_start=0):
    MidStation.objects.all().delete()
    Train.objects.all().delete()
    
    with open(os.path.join(SPIDER_DATA_DIRNAME, 'train_spider_all', '火车班次json数据.json'), 'r', encoding='utf-8') as file:
        bar = tqdm(list(enumerate(file.readlines())), dynamic_ncols=True)
    mid_sta_objs = []
    for line, result in bar:
        bar.set_description(f'[line{line}]')
        if line < line_start:
            continue
        try:
            result = json.loads(result)
        except:
            result = None
        if result:
            train_num = list(result['trainInfo'].keys())[0]
            dept_city_name = result['trainInfo'][train_num]['deptCity']
            arri_city_name = result['trainInfo'][train_num]['arriCity']
            
            bar.set_postfix_str(f'{dept_city_name} => {arri_city_name}')
            
            dept_city = City.get_via_name(dept_city_name)
            arri_city = City.get_via_name(arri_city_name)
            if dept_city is None or arri_city is None:
                continue
            
            dept_sta, _ = Station.objects.get_or_create(
                name_ch=result['trainInfo'][train_num]['deptStation'],
                defaults=dict(jingdu=dept_city.jingdu, weidu=dept_city.weidu, city=dept_city)
            )
            arri_sta, _ = Station.objects.get_or_create(
                name_ch=result['trainInfo'][train_num]['arriStation'],
                defaults=dict(jingdu=arri_city.jingdu, weidu=arri_city.weidu, city=arri_city)
            )
            train = Train.objects.create(
                name=train_num,
                dept_date=result['trainInfo'][train_num]['dptDate'],
                dept_time=result['trainInfo'][train_num]['deptTime'],
                arri_date=result['trainInfo'][train_num]['arrDate'],
                arri_time=result['trainInfo'][train_num]['arriTime'],
                dept_station=dept_sta,
                arri_station=arri_sta,
                dept_city=dept_city,
                arri_city=arri_city,
                interval=result['extInfo']['allTime'],
                kilometer=result['extInfo']['allMileage'],
            )
            
            mid_list = result['trainScheduleBody']
            mid_list.sort(key=lambda ci: ci['content'][-4])
            mid_list = list(filter(lambda ci: City.get_via_name(ci['content'][1]) is not None, mid_list))
            for index, c in enumerate(mid_list):
                content = c['content']
                city = City.get_via_name(content[1])
                sta, flag = Station.objects.get_or_create(
                    name_ch=content[1], defaults=dict(
                        jingdu=city.jingdu,
                        weidu=city.weidu,
                        city=city,
                    )
                )
                mid_sta_objs.append(MidStation(
                    index=index + 1,
                    arri_date=content[2],
                    arri_time=content[3],
                    station=sta, train=train
                ))
        else:
            bar.set_postfix_str(f'failed!')
    MidStation.objects.bulk_create(mid_sta_objs, batch_size=BULK_CREATE_BATCH_SIZE)


if __name__ == '__main__':
    train_import()
