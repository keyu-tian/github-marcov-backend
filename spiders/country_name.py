import json
import os
from xml.dom.minidom import parse
import xml.dom.minidom


def get_input_options_by_xml(path):
    DOMTree = xml.dom.minidom.parse("./CountryProvinceCityLocListCH_and_Code.xml")
    glo = DOMTree.documentElement.getElementsByTagName('CountryRegion')
    res = {'country': []}
    for i in range(len(glo)):
        country = glo.item(i).getAttribute('Name')
        res['country'].append(country)
    with open(os.path.join(path, './country_list.json'), 'a', encoding='utf-8') as fp:
    # with open('./country_list.py', 'a', encoding='utf-8') as fp:
        fp.write(json.dumps(res) + '\n')
    return res


if __name__ == '__main__':
    get_input_options_by_xml('')