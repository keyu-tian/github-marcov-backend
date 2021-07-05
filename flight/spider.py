import time
import re
import json

from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from multiprocessing.pool import ThreadPool

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument(
    f'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')

area_list = ''
code_to_name = {}
today = datetime.now().strftime('%Y-%m-%d')
# 单线程
NUM_THREADS = 1

# 核心城市
kernel = '兰州 西宁 西安 郑州 济南 太原 合肥 长沙 武汉 南京 成都 贵阳 昆明 哈尔滨 长春 沈阳 石家庄 杭州 南昌 广州 福州 台北 海口 北京 天津 上海 重庆 南宁 拉萨 银川 乌鲁木齐 呼和浩特 香港 澳门'.split()
with open('flight.txt', 'r+', encoding='utf-8') as f:
    city_list = re.split(',', f.read().replace(' ', '').replace('\n', ''))[1:-1]
    # print(city_list)
    for x in city_list:
        city_name, res_code = x.split(':')
        city_name = city_name[1:-1]
        res_code = res_code[1:-1]
        if city_name in kernel:
            code_to_name[res_code] = city_name


def get_flight_info(ind):
    results = []
    driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=options)
    for src in list(code_to_name.keys())[ind: len(city_list): NUM_THREADS]:
        print(src)
        for dst in list(code_to_name.keys()):
            if src == dst:
                continue
            url = f'http://www.umetrip.com/mskyweb/fs/fa.do?dep={src}&arr={dst}&date={today}&channel='  # time:2021-07-02
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
                    if fail_num > 1:
                        break
                    driver.refresh()
                    continue
                fail_num = 0
                for flight in flights:
                    context = flight.get_text().strip().split()
                    # print(context)
                    results.append({'code': context[0][:-4], 'dept_time': today + ' ' + (context[1] if context[2] == "--" else context[2]) + ':00', 'arri_time': today + ' ' + (context[4] if context[5] == "--" else context[5]) + ':00', 'condition': context[6], 'dept_city': src, 'arri_city': dst})
                try:
                    next_page = driver.find_element_by_css_selector('#p_next')
                    next_page.click()
                except:
                    break
    driver.quit()
    return results


# with ThreadPool(NUM_THREADS) as pool:
#     args = list(range(0, NUM_THREADS))
#     ret = list(pool.imap(get_flight_info, args))
def main():
    start = time.time()
    ret = get_flight_info(0)
    with open('./flights_data.json', 'w+', encoding='utf-8') as f:
        f.write(json.dumps(ret, ensure_ascii=False))

    end = time.time()
    print(f'cost time: {end - start}s')


main()
