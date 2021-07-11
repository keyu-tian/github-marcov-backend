import os
import time

import requests
import json
from lxml import etree
from tqdm import tqdm

from meta_config import SPIDER_DATA_DIRNAME


def train_spider_new():
    url = "https://trains.ctrip.com/TrainSchedule/"
    with open(os.path.join(SPIDER_DATA_DIRNAME, 'train_spider_all', '火车班次列表.json'), 'r', encoding='utf-8') as file:
        bar = tqdm(list(enumerate(file.readlines())), dynamic_ncols=True)
    for line, result in bar:
        bar.set_description(f'[line{line}], reslut{result.strip()}')
        get_url = url + result.strip()
        res = requests.get(get_url)
        time.sleep(0.1)
        tree = etree.HTML(res.content.decode("utf-8"))
        if len(tree.xpath('//*[@id="ctl00_MainContentPlaceHolder_pnlResult"]/div[2]/table[1]/tbody/tr/td[1]')) == 0:
            continue
        save_json = {
            "trainInfo": {
                result.strip(): {
                    "arriTime": tree.xpath('//*[@id="ctl00_MainContentPlaceHolder_pnlResult"]/div[2]/table[1]/tbody/tr/td[5]')[0].text.strip(),
                    "code": result.strip(),
                    "deptCity": tree.xpath('//*[@id="startStationName"]')[0].text.strip(),
                    "deptTime": tree.xpath('//*[@id="ctl00_MainContentPlaceHolder_pnlResult"]/div[2]/table[1]/tbody/tr/td[4]')[0].text.strip(),
                    "arriCity": "",
                    "arriStation": tree.xpath('//*[@id="ctl00_MainContentPlaceHolder_pnlResult"]/div[2]/table[1]/tbody/tr/td[3]')[0].text.strip(),
                    "deptStation": "",
                    "interval": tree.xpath('//*[@id="ctl00_MainContentPlaceHolder_pnlResult"]/div[2]/table[1]/tbody/tr/td[6]')[0].text.strip(),
                }
            },
            "extInfo": {
                "allTime": tree.xpath('//*[@id="ctl00_MainContentPlaceHolder_pnlResult"]/div[2]/table[1]/tbody/tr/td[6]')[0].text.strip(),
                "allMileage": "未知",
            },
            "trainScheduleBody": [
                {"content": ["",
                             tree.xpath(f'//*[@id="ctl00_MainContentPlaceHolder_pnlResult"]/div[2]/table[2]/tbody/tr[{i + 1}]/td[3]')[0].text.strip(),
                             tree.xpath(f'//*[@id="ctl00_MainContentPlaceHolder_pnlResult"]/div[2]/table[2]/tbody/tr[{i + 1}]/td[2]')[0].text.strip(),
                             tree.xpath(f'//*[@id="ctl00_MainContentPlaceHolder_pnlResult"]/div[2]/table[2]/tbody/tr[{i + 1}]/td[4]')[0].text.strip(),
                             tree.xpath(f'//*[@id="ctl00_MainContentPlaceHolder_pnlResult"]/div[2]/table[2]/tbody/tr[{i + 1}]/td[5]')[0].text.strip()]}
                for i in range(len(tree.xpath('//*[@id="ctl00_MainContentPlaceHolder_pnlResult"]/div[2]/table[2]/tbody/*')))
            ]
        }
        with open('火车班次json数据.json', 'a', encoding='utf-8') as fp:
            fp.write(json.dumps(save_json) + '\n')


if __name__ == '__main__':
    train_spider_new()