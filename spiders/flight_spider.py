import time
import re
import json
import os
import argparse

from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver

from meta_config import SPIDER_DATA_DIRNAME


def get_flight_info(begin_pos, city_list, code, args, options):
    if begin_pos[0] == len(city_list)-1 and begin_pos[1] == len(city_list)-1:
        print('该天的航班爬取已完成')
        return
    driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=options)
    now = datetime.now().strftime("%Y-%m-%d")
    for src in code[begin_pos[0]: len(city_list)]:
        print(code.index(src))
        for dst in code[begin_pos[1]: len(city_list)]:
            if src == dst:
                continue
            results = []
            url = f'http://www.umetrip.com/mskyweb/fs/fa.do?dep={src}&arr={dst}&date={args.date if args.date else now}&channel='  # time:2021-07-02
            driver.get(url)
            fail_num = 0
            while True:
                elem = driver.find_element_by_xpath("//*")
                source_code = elem.get_attribute("outerHTML")
                soup = BeautifulSoup(source_code, 'html.parser')
                flights = soup.find_all(attrs={'class': 'li_com'})
                err = soup.find_all(attrs={'class': 'err_com'})
                if len(err) > 0:
                    fail_num += 1
                    if fail_num > 5:
                        break
                    driver.refresh()
                    continue
                fail_num = 0
                for flight in flights:
                    context = flight.get_text().strip().split()
                    # print(context)
                    results.append({'code': ''.join(re.findall(r'[A-Za-z0-9]', context[0])), 'dept_time': now + ' ' + (context[1] if context[2] == "--" else context[2]) + ':00', 'arri_time': now + ' ' + (context[4] if context[5] == "--" else context[5]) + ':00', 'condition': context[6], 'dept_city': src, 'arri_city': dst})
                try:
                    next_page = driver.find_element_by_css_selector('#p_next')
                    next_page.click()
                except:
                    break
            # print(results)
            if begin_pos[0] == 0 and begin_pos[1] == 0:
                # with open(f'/{SPIDER_DATA_DIRNAME}/flights_data/flights_data{now}.json', 'r+', encoding='utf-8') as fp:
                #     context_now = fp.read()
                #     if context_now == '':
                #         context_now = []
                #     else:
                #         context_now = json.loads(context_now)
                with open(f'{SPIDER_DATA_DIRNAME}/flights_data/flights_data{now}.json', 'w+', encoding='utf-8') as fp:
                    # context_now.extend(results)
                    fp.write(json.dumps(results, ensure_ascii=False))
            else:
                with open(f'{SPIDER_DATA_DIRNAME}/flights_data/flights_data{args.date}.json', 'r+', encoding='utf-8') as fp:
                    context_now = fp.read()
                    if context_now == '':
                        context_now = []
                    else:
                        context_now = json.loads(context_now)
                with open(f'{SPIDER_DATA_DIRNAME}/flights_data/flights_data{args.date}.json', 'w+', encoding='utf-8') as fp:
                    context_now.extend(results)
                    fp.write(json.dumps(context_now, ensure_ascii=False))
    driver.quit()


def main():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument(
        f'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
    
    parser = argparse.ArgumentParser(description='Flight-Spider')
    parser.add_argument('--date', required=False, type=str)
    args = parser.parse_args()
    code = []
    
    # 核心城市
    # kernel = '兰州 西宁 西安 郑州 济南 太原 合肥 长沙 武汉 南京 成都 贵阳 昆明 哈尔滨 长春 沈阳 石家庄 杭州 南昌 广州 福州 台北 海口 北京 天津 上海 重庆 南宁 拉萨 银川 乌鲁木齐 呼和浩特 香港 澳门'.split()
    with open('spiders/flight.txt', 'r+', encoding='utf-8') as f:
        city_list = re.split(',', f.read().replace(' ', '').replace('\n', ''))[1:-1]
        for x in city_list:
            city_name, res_code = x.split(':')
            res_code = res_code[1:-1]
            code.append(res_code)
            
    start = time.time()
    begin_pos = [0, 0]
    if args.date:
        try:
            with open(f'{SPIDER_DATA_DIRNAME}/flights_data/flights_data{args.date}.json', 'r+', encoding='utf-8') as f:
                context = json.loads(f.read())[-1]
                begin_pos[0] = code.index(context['dept_city'])
                begin_pos[1] = code.index(context['arri_city'])
        except:
            print('您选择的日期错误（日期格式：y-m-d，例如：2020-07-02')
    else:
        try:
            with open(f'{SPIDER_DATA_DIRNAME}/flights_data/flights_data{datetime.now().strftime("%Y-%m-%d")}.json', 'r+', encoding='utf-8') as f:
                context = json.loads(f.read())[-1]
                begin_pos[0] = code.index(context['dept_city'])
                begin_pos[1] = code.index(context['arri_city'])
        except FileNotFoundError:
            pass
    print('begin_pos:', begin_pos[0], begin_pos[1])
    get_flight_info(begin_pos, city_list, code, args, options)
    end = time.time()
    print(f'cost time: {end - start}s')


if __name__ == '__main__':
    main()
