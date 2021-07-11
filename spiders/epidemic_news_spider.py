import time

import os
from selenium import webdriver


def spider(path):
    assert os.path.sep == '\\', '这个代码只能在windows上运行哈'
    driver = webdriver.Chrome(executable_path='chromedriver.exe')

    driver.implicitly_wait(10)

    driver.get('http://wx.wind.com.cn/unitedweb/cmsapp/Sites/sariInfo/message.html?from=timeline&isappinstalled=0')
    time.sleep(10)
    js = 'var q=document.documentElement.scrollTop=20000'
    driver.execute_script(js)
    time.sleep(10)
    ul_element1 = driver.find_elements_by_xpath('//*[@id="root"]/div/div/div[19]/div/div[3]/ul')[0]
    # 获取li
    ul_child_list1 = ul_element1.find_elements_by_xpath('./li')
    for i in range(len(ul_child_list1)):
        # 获取div[3]
        ul_child_list_datetime = ul_child_list1[i].find_elements_by_xpath('./div[4]/div[1]/div[1]')[0]  #
        ul_child_list_datetime_str = ul_child_list_datetime.text
        ul_child_list_a = ul_child_list1[i].find_elements_by_xpath('./div[4]/div[1]/div[2]/a')[0]
        ul_child_list_a_content = ul_child_list_a.text
        ul_child_list_a_href = ul_child_list_a.get_attribute('href')
        with open(os.path.join(path, 'epidemic_news.json'), 'r+', encoding='utf-8') as f:
            old = f.read()
            f.seek(0)
            f.write(f'{{"date": "{ul_child_list_datetime_str}", "content": "{ul_child_list_a_content}", "src": "{ul_child_list_a_href}"}}\n')
            f.write(old)

    js = 'var q=document.documentElement.scrollTop=15000'
    driver.execute_script(js)
    time.sleep(10)

    ul_element2 = driver.find_elements_by_xpath('//*[@id="root"]/div/div/div[21]/div/div[3]/ul')[0]
    # 获取li
    ul_child_list2 = ul_element2.find_elements_by_xpath('./li')
    for i in range(len(ul_child_list2)):
        # 获取div[3]
        ul_child_list_datetime = ul_child_list2[i].find_elements_by_xpath('./div[4]/div[1]/div[1]')[0]  #
        ul_child_list_datetime_str = ul_child_list_datetime.text
        ul_child_list_a = ul_child_list2[i].find_elements_by_xpath('./div[4]/div[1]/div[2]/a')[0]
        ul_child_list_a_content = ul_child_list_a.text
        ul_child_list_a_href = ul_child_list_a.get_attribute('href')
        with open(os.path.join(path, 'government_news.json'), 'a', encoding='utf-8') as fp:
            fp.write(f'{{"date": "{ul_child_list_datetime_str}", "content": "{ul_child_list_a_content}", "src": "{ul_child_list_a_href}"}}\n')

    driver.close()


if __name__ == '__main__':
    spider('./')