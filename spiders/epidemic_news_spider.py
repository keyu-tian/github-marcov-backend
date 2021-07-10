import time

from coverage.annotate import os
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait


def spider(path):
    driver = webdriver.Chrome(executable_path='chromedriver.exe')

    driver.implicitly_wait(10)

    driver.get('http://wx.wind.com.cn/unitedweb/cmsapp/Sites/sariInfo/message.html?from=timeline&isappinstalled=0')
    for i in range(2):
        js = 'var q=document.documentElement.scrollTop=10000'
        driver.execute_script(js)
        time.sleep(3)

    element = WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div[19]/div/div[3]/ul'))
        )
    res = element.text.split('\n')
    for i in range(int(len(res) / 2)):
        with open(os.path.join(path, 'epidemic_news.json'), 'a', encoding='utf-8') as fp:
            fp.write(f'{{"date": "{res[i * 2]}", "content": "{res[i * 2 + 1]}"}}\n')
    element = WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div[21]/div/div[3]/ul'))
    )
    res = element.text.split('\n')
    for i in range(int(len(res) / 2)):
        with open(os.path.join(path, 'government_news.json'), 'a', encoding='utf-8') as fp:
            fp.write(f'{{"date": "{res[i * 2]}", "content": "{res[i * 2 + 1]}"}}\n')
    print(element.text)
    driver.close()


if __name__ == '__main__':
    spider('./')