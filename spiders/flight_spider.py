import time
import re
import json
import requests
from datetime import datetime

from meta_config import SPIDER_DATA_DIRNAME


code = ['PEK', 'PVG', 'CAN', 'PKX', 'SHA', 'MFM', 'SZX', 'CSX', 'KMG', 'SWA', 'HGH', 'HKG', 'CKG', 'CTU', 'XIY', 'CGQ', 'NKG', 'HFE', 'KHN', 'CGO', 'KWE', 'TNA', 'ZUH', 'WUH', 'HAK', 'NNG', 'HRB', 'XMN', 'FOC', 'URC', 'LXA', 'SYX', 'SHE', 'NGB', 'LHW', 'TSN', 'DLC', 'INC', 'ZYI', 'TPE', 'HET', 'SJW', 'WDS', 'KWL', 'JJN', 'TAO', 'HLD', 'YNT', 'KHH', 'CZX', 'TYN', 'WUX', 'HIA', 'WNZ', 'NAY', 'HYN', 'WGN', 'NTG', 'LJG', 'HNY', 'YBP', 'DLU', 'BZX', 'DYG', 'YSQ', 'TSA', 'XNN', 'BHY', 'XUZ', 'MIG', 'TXN', 'JHG', 'XFN', 'WEH', 'KOW', 'DNH', 'HUZ', 'YIH', 'DSN', 'NNY', 'AHJ', 'ZHA', 'JZH', 'RMQ', 'AOG', 'DQA', 'BAV', 'JNG', 'LYG', 'LZN', 'HZG', 'JGS', 'LFQ', 'SZV', 'HSN', 'LYI', 'GHN', 'DOY', 'LYA', 'SQD', 'WXN', 'MXZ', 'YIC', 'ENH', 'JUH', 'LCX', 'FUG', 'HPG', 'NAO', 'LZH', 'ERL', 'CIH', 'MZG', 'CGD', 'JNZ', 'ACX', 'GYS', 'NBS', 'LZY', 'HDG', 'AEB', 'NDG', 'KHG', 'KRY', 'CIF', 'HTN', 'MDG', 'ZAT', 'HJJ', 'JIC', 'PZI', 'CNI', 'FUO', 'JDZ', 'HUN', 'KRL', 'JMU', 'BPX', 'TNN', 'TVS', 'DAX', 'DDG', 'KNH', 'XIC', 'AKA', 'LUM', 'HZH', 'JGN', 'AKU', 'DIG', 'WUS', 'TTT', 'AVA', 'TCZ', 'LZO', 'DAT', 'NGQ', 'SHS', 'WOT', 'WEF', 'AAT', 'TGO', 'JIL', 'SHP', 'GOQ', 'JIQ', 'AQG', 'WUZ', 'HLH', 'CHG', 'YIE', 'BPL', 'OHE', 'GYU', 'SYM', 'JIU', 'KCA', 'CMJ', 'ZHY', 'FYN', 'TNH', 'BSD', 'HCN', 'HHP', 'MFK', 'DGM', 'LNJ', 'XIL', 'THQ', 'IQN', 'CYI', 'JUZ', 'YUS', 'PIF', 'WUA', 'HEK', 'HMI', 'BFU', 'JGD', 'AYN', 'KTZ', 'TXG', 'CHW', 'DZU', 'XNT', 'HSC', 'TCG', 'LHN', 'IQM', 'GNI', 'HSZ', 'KYD', 'SMT', 'SXJ', 'LXI']
foreign_code = ['NRT', 'HND', 'ITM', 'KIX', 'ICN', 'PUS', 'SIN', 'KUL', 'SGN', 'BKK', 'DEL', 'THR', 'RUH', 'AUH', 'DXB', 'DOH', 'IST', 'YOW', 'YUL', 'YVR', 'YYZ', 'IAD', 'BOS', 'ORD', 'JFK', 'SFO', 'LAX', 'MIA', 'ATL', 'CAE', 'CLE', 'CLT', 'DEN', 'DFW', 'DTW', 'IAH', 'MCO', 'MEM', 'SEA', 'LHR', 'LPL', 'MAN', 'BRU', 'LUX', 'AMS', 'RTM', 'CPH']


def get_flight_info_two_area(src, dst):
    now = datetime.now().strftime("%Y-%m-%d")
    url = f'http://www.umetrip.com/mskyweb/fs/fa.do?dep={src}&arr={dst}&date={now}&channel='  # time:2021-07-02
    response = requests.get(url)
    text = response.text.replace('"', '')
    aim1 = 'temp.push'
    aim2 = 'i\+\+'
    position1 = []
    position2 = []
    for pos in re.finditer(aim1, text):
        position1.append(pos.span()[0])
    for pos in re.finditer(aim2, text):
        position2.append(pos.span()[0])
    t = 1
    for start_pos, end_pos in zip(position1, position2):
        if t > 1:
            break
        t += 1
        section = text[start_pos: end_pos]
        split_ans = re.split('[<>]', section)
        flight_code = split_ans[12]
        dept_time = split_ans[26].strip()
        arri_time = split_ans[38][1:].strip()
        date = split_ans[51].strip()[-11:-1]
        condition = split_ans[46][1:].strip()
        return {'code': flight_code,
                'dept_time': date + ' ' + dept_time,
                'arri_time': date + ' ' + arri_time,
                'condition': condition, 'dept_city': src, 'arri_city': dst}
    return {'code': '0'}


def get_flight_info():
    now = datetime.now().strftime("%Y-%m-%d")
    results = []
    total_num = len(code) + len(foreign_code)
    finished = 0
    for src in code:
        for dst in code:
            res = get_flight_info_two_area(src, dst)
            if res['code'] != '0':
                results.append(res)
        finished += 1
        print(f'已完成 {finished}/{total_num}')
    for src in foreign_code:
        for dst in code:
            res = get_flight_info_two_area(src, dst)
            if res['code'] != '0':
                results.append(res)
            res = get_flight_info_two_area(dst, src)
            if res['code'] != '0':
                results.append(res)
        finished += 1
        print(f'已完成 {finished}/{total_num}')

    with open(f'{SPIDER_DATA_DIRNAME}/flights_data{now}.json', 'w+', encoding='utf-8') as fp:
        fp.write(json.dumps(results, ensure_ascii=False))


def main():
    start = time.time()
    get_flight_info()
    end = time.time()
    print(f'cost time: {end - start}s')


if __name__ == '__main__':
    main()
