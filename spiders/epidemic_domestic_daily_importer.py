import datetime as dt
import json
import os
import requests
from utils.dict_ch import city_dict_ch, province_dict_ch
from meta_config import SPIDER_DATA_DIRNAME

from tqdm import tqdm

city_new_to_old = {
    '东城': '东城区',
    '西城': '西城区',
    '朝阳': '朝阳区',
    '丰台': '丰台区',
    '石景山': '石景山区',
    '海淀': '海淀区',
    '门头沟': '门头沟区',
    '房山': '房山区',
    '通州': '通州区',
    '顺义': '顺义区',
    '昌平': '昌平区',
    '大兴': '大兴区',
    '怀柔': '怀柔区',
    '密云': '密云区',
    '延庆': '延庆区',
    '万州区': '万州区',
    '涪陵区': '涪陵区',
    '渝中区': '渝中区',
    '大渡口区': '大渡口区',
    '江北区': '江北区',
    '沙坪坝区': '沙坪坝区',
    '九龙坡区': '九龙坡区',
    '南岸区': '南岸区',
    '綦江区': '綦江区',
    '大足区': '大足区',
    '渝北区': '渝北区',
    '巴南区': '巴南区',
    '黔江区': '黔江区',
    '长寿区': '长寿区',
    '江津区': '江津区',
    '合川区': '合川区',
    '永川区': '永川区',
    '璧山区': '璧山区',
    '铜梁区': '铜梁区',
    '潼南区': '潼南区',
    '荣昌区': '荣昌区',
    '城口县': '城口县',
    '丰都县': '丰都县',
    '垫江县': '垫江县',
    '忠县': '忠县',
    '云阳县': '云阳县',
    '奉节县': '奉节县',
    '巫山县': '巫山县',
    '巫溪县': '巫溪县',
    '开州区': '开州区',
    '金昌': '金昌市',
    '白银': '白银市',
    '天水': '天水市',
    '平凉': '平凉市',
    '河源': '河源市',
    '琼海': '琼海市',
    '东方': '东方市',
    '澄迈县': '澄迈县',
    '临高县': '临高县',
    '邯郸': '邯郸市',
    '安阳': '安阳市',
    '鹤壁': '鹤壁市',
    '漯河': '漯河市',
    '神农架': '神农架林区',
    '吉林': '吉林市',
    '四平': '四平市',
    '抚顺': '抚顺市',
    '包头': '包头市',
    '乌海': '乌海市',
    '赤峰': '赤峰市',
    '通辽': '通辽市',
    '呼伦贝尔': '呼伦贝尔市',
    '兴安盟': '兴安盟',
    '锡林郭勒': '锡林郭勒盟',
    '西宁': '西宁市',
    '淄博': '淄博市',
    '黄浦': '黄浦区',
    '徐汇': '徐汇区',
    '长宁': '长宁区',
    '静安': '静安区',
    '普陀': '普陀区',
    '虹口': '虹口区',
    '杨浦': '杨浦区',
    '闵行': '闵行区',
    '宝山': '宝山区',
    '嘉定': '嘉定区',
    '浦东': '浦东新区',
    '金山': '金山区',
    '松江': '松江区',
    '青浦': '青浦区',
    '奉贤': '奉贤区',
    '崇明': '崇明区',
    '朔州': '朔州市',
    '临汾': '临汾市',
    '和平区': '和平区',
    '河东区': '河东区',
    '河西区': '河西区',
    '南开区': '南开区',
    '河北区': '河北区',
    '红桥区': '红桥区',
    '东丽区': '东丽区',
    '西青区': '西青区',
    '津南区': '津南区',
    '北辰区': '北辰区',
    '武清区': '武清区',
    '宝坻区': '宝坻区',
    '滨海新区': '滨海新区',
    '宁河区': '宁河区',
    '吐鲁番': '吐鲁番市',
    '阿克苏': '阿克苏地区',
    '喀什': '喀什地区',
    '第八师石河子': '石河子市',
    '六师五家渠': '五家渠市',
    '丽江市': '丽江市',
    '兰州': '兰州市',
    '定西': '定西市',
    '陇南': '陇南市',
    '庆阳': '庆阳市',
    '临夏': '临夏回族自治州',
    '张掖': '张掖市',
    '福州': '福州市',
    '莆田': '莆田市',
    '泉州': '泉州市',
    '厦门': '厦门市',
    '宁德': '宁德市',
    '漳州': '漳州市',
    '南平': '南平市',
    '三明': '三明市',
    '龙岩': '龙岩市',
    '南宁': '南宁市',
    '北海': '北海市',
    '桂林': '桂林市',
    '河池': '河池市',
    '柳州': '柳州市',
    '防城港': '防城港市',
    '玉林': '玉林市',
    '来宾': '来宾市',
    '钦州': '钦州市',
    '贵港': '贵港市',
    '梧州': '梧州市',
    '贺州': '贺州市',
    '百色': '百色市',
    '德宏州': '德宏傣族景颇族自治州',
    '昆明': '昆明市',
    '昭通市': '昭通市',
    '玉溪': '玉溪市',
    '曲靖': '曲靖市',
    '大理': '大理白族自治州',
    '红河': '红河哈尼族彝族自治州',
    '保山市': '保山市',
    '普洱': '普洱市',
    '楚雄州': '楚雄彝族自治州',
    '文山州': '文山壮族苗族自治州',
    '临沧': '临沧市',
    '广州': '广州市',
    '深圳': '深圳市',
    '佛山': '佛山市',
    '珠海': '珠海市',
    '江门': '江门市',
    '东莞': '东莞市',
    '肇庆': '肇庆市',
    '阳江': '阳江市',
    '中山': '中山市',
    '惠州': '惠州市',
    '湛江': '湛江市',
    '汕头': '汕头市',
    '梅州': '梅州市',
    '茂名': '茂名市',
    '清远': '清远市',
    '揭阳': '揭阳市',
    '韶关': '韶关市',
    '潮州': '潮州市',
    '汕尾': '汕尾市',
    '成都': '成都市',
    '甘孜': '甘孜藏族自治州',
    '达州': '达州市',
    '南充': '南充市',
    '广安': '广安市',
    '泸州': '泸州市',
    '巴中': '巴中市',
    '绵阳': '绵阳市',
    '内江': '内江市',
    '德阳': '德阳市',
    '遂宁': '遂宁市',
    '攀枝花': '攀枝花市',
    '凉山': '凉山彝族自治州',
    '宜宾': '宜宾市',
    '自贡': '自贡市',
    '眉山': '眉山市',
    '雅安': '雅安市',
    '广元': '广元市',
    '资阳': '资阳市',
    '乐山': '乐山市',
    '阿坝': '阿坝藏族羌族自治州',
    '大连': '大连市',
    '沈阳': '沈阳市',
    '锦州': '锦州市',
    '葫芦岛': '葫芦岛市',
    '丹东': '丹东市',
    '盘锦': '盘锦市',
    '营口': '营口市',
    '阜新': '阜新市',
    '铁岭': '铁岭市',
    '鞍山': '鞍山',  # TODO: 前端的鞍山叫什么？
    '马鞍山': '马鞍山市',
    '本溪': '本溪市',
    '辽阳': '辽阳市',
    '西安': '西安市',
    '安康': '安康市',
    '汉中': '汉中市',
    '咸阳': '咸阳市',
    '渭南': '渭南市',
    '宝鸡': '宝鸡市',
    '延安': '延安市',
    '铜川': '铜川市',
    '商洛': '商洛市',
    '榆林': '榆林市',
    '南京': '南京市',
    '苏州': '苏州市',
    '徐州': '徐州市',
    '淮安': '淮安市',
    '无锡': '无锡市',
    '常州': '常州市',
    '连云港': '连云港市',
    '南通': '南通市',
    '泰州': '泰州市',
    '盐城': '盐城市',
    '扬州': '扬州市',
    '宿迁': '宿迁市',
    '镇江': '镇江市',
    '长沙': '长沙市',
    '岳阳': '岳阳市',
    '邵阳': '邵阳市',
    '常德': '常德市',
    '株洲': '株洲市',
    '娄底': '娄底市',
    '益阳': '益阳市',
    '衡阳': '衡阳市',
    '永州': '永州市',
    '怀化': '怀化市',
    '郴州': '郴州市',
    '湘潭': '湘潭市',
    '湘西自治州': '湘西土家族苗族自治州',
    '张家界': '张家界市',
    '武汉': '武汉市',
    '孝感': '孝感市',
    '黄冈': '黄冈市',
    '荆州': '荆州市',
    '鄂州': '鄂州市',
    '随州': '随州市',
    '襄阳': '襄阳市',
    '黄石': '黄石市',
    '宜昌': '宜昌市',
    '荆门': '荆门市',
    '咸宁': '咸宁市',
    '十堰': '十堰市',
    '仙桃': '仙桃市',
    '天门': '天门市',
    '恩施州': '恩施土家族苗族自治州',
    '潜江': '潜江市',
    '合肥': '合肥市',
    '蚌埠': '蚌埠市',
    '阜阳': '阜阳市',
    '亳州': '亳州市',
    '安庆': '安庆市',
    '六安': '六安市',
    '宿州': '宿州市',
    '芜湖': '芜湖市',
    '铜陵': '铜陵市',
    '淮北': '淮北市',
    '淮南': '淮南市',
    '池州': '池州市',
    '滁州': '滁州市',
    '黄山': '黄山市',
    '宣城': '宣城市',
    '济宁': '济宁市',
    '青岛': '青岛市',
    '临沂': '临沂市',
    '济南': '济南市',
    '烟台': '烟台市',
    '潍坊': '潍坊市',
    '威海': '威海市',
    '聊城': '聊城市',
    '德州': '德州市',
    '泰安': '泰安市',
    '枣庄': '枣庄市',
    '菏泽': '菏泽市',
    '日照': '日照市',
    '滨州': '滨州市',
    '鄂尔多斯': '鄂尔多斯市',
    '巴彦淖尔': '巴彦淖尔市',
    '呼和浩特': '呼和浩特市',
    '乌兰察布': '乌兰察布市',
    '温州': '温州市',
    '杭州': '杭州市',
    '宁波': '宁波市',
    '台州': '台州市',
    '金华': '金华市',
    '嘉兴': '嘉兴市',
    '绍兴': '绍兴市',
    '丽水': '丽水市',
    '衢州': '衢州市',
    '湖州': '湖州市',
    '舟山': '舟山市',
    '信阳': '信阳市',
    '郑州': '郑州市',
    '南阳': '南阳市',
    '驻马店': '驻马店市',
    '商丘': '商丘市',
    '周口': '周口市',
    '平顶山': '平顶山市',
    '新乡': '新乡市',
    '许昌': '许昌市',
    '焦作': '焦作市',
    '洛阳': '洛阳市',
    '开封': '开封市',
    '濮阳': '濮阳市',
    '三门峡': '三门峡市',
    '石柱县': '石柱土家族自治县',
    '彭水县': '彭水苗族土家族自治县',
    '秀山县': '秀山土家族苗族自治县',
    '酉阳县': '酉阳土家族苗族自治县',
    '晋中': '晋中市',
    '太原': '太原市',
    '运城': '运城市',
    '大同': '大同市',
    '晋城': '晋城市',
    '长治': '长治市',
    '忻州': '忻州市',
    '吕梁': '吕梁市',
    '阳泉': '阳泉市',
    '绥化': '绥化市',
    '哈尔滨': '哈尔滨市',
    '双鸭山': '双鸭山市',
    '鸡西': '鸡西市',
    '齐齐哈尔': '齐齐哈尔市',
    '牡丹江': '牡丹江市',
    '大庆': '大庆市',
    '黑河': '黑河市',
    '七台河': '七台河市',
    '佳木斯': '佳木斯市',
    '鹤岗': '鹤岗市',
    '大兴安岭': '大兴安岭地区',
    '伊春': '伊春市',
    '三亚': '三亚市',
    '海口': '海口市',
    '儋州': '儋州市',
    '万宁': '万宁市',
    '定安县': '定安县',
    '文昌': '文昌市',
    '保亭': '保亭黎族苗族自治县',
    '乐东': '乐东黎族自治县',
    '银川': '银川市',
    '吴忠': '吴忠市',
    '固原': '固原市',
    '中卫': '中卫市',
    '石嘴山': '石嘴山市',
    '保定': '保定市',
    '石家庄': '石家庄市',
    '邢台': '邢台市',
    '唐山': '唐山市',
    '沧州': '沧州市',
    '张家口': '张家口市',
    '廊坊': '廊坊市',
    '秦皇岛': '秦皇岛市',
    '衡水': '衡水市',
    '承德': '承德市',
    '海北州': '海北藏族自治州',
    '南昌': '南昌市',
    '新余': '新余市',
    '上饶': '上饶市',
    '九江': '九江市',
    '宜春': '宜春市',
    '赣州': '赣州市',
    '抚州': '抚州市',
    '萍乡': '萍乡市',
    '吉安': '吉安市',
    '鹰潭': '鹰潭市',
    '景德镇': '景德镇市',
    '通化': '通化市',
    '长春': '长春市',
    '辽源': '辽源市',
    '延边': '延边朝鲜族自治州',
    '松原': '松原市',
    '白城': '白城市',
    '拉萨': '拉萨市',
    '乌鲁木齐': '乌鲁木齐市',
    '伊犁州': '伊犁哈萨克自治州',
    '昌吉州': '昌吉回族自治州',
    '巴州': '巴音郭楞蒙古自治州',
    '贵阳': '贵阳市',
    '遵义': '遵义市',
    '毕节': '毕节市',
    '黔南州': '黔西南布依族苗族自治州',
    '六盘水': '六盘水市',
    '铜仁': '铜仁市',
    '黔东南州': '黔东南苗族侗族自治州',
    '安顺': '安顺市',
    '甘南州': '甘南藏族自治州',
    '西双版纳州': '西双版纳傣族自治州',
    '济源示范区': '济源市',
    '昌江县': '昌江黎族自治县',
    '陵水县': '陵水黎族自治县',
    '琼中县': '琼中黎族苗族自治县',
}


def epidemic_domestic_daily_import():

    # 获取数据
    # daily_data = json.load(open(os.path.join(SPIDER_DATA_DIRNAME, 'epidemic_domestic_data', '2021-07-09.json'), 'r', encoding='utf-8'))
    # r = open(os.path.join(SPIDER_DATA_DIRNAME, 'epidemic_domestic_data', '2021-07-10.json')).read()
    print('[loading]')
    r = requests.get('https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5')
    daily_data = json.loads(r.text.replace('\\', '').replace('"{', '{').replace('}"', '}'))
    today_provinces_data_list = daily_data['data']['areaTree'][0]['children']
    today_provinces_data = {}
    for it in today_provinces_data_list:
        today_provinces_data[it['name']] = it
        today_cities_data = {}
        for it2 in it['children']:
            if '境外' in it2['name']:
                it2['name'] += '-' + it['name']
            if '外地' in it2['name']:
                it2['name'] += '-' + it['name']
            if '确认' in it2['name']:
                it2['name'] += '-' + it['name']
            if it2['name'] in city_new_to_old.keys():
                it2['name'] = city_new_to_old[it2['name']]
                today_cities_data[it2['name']] = it2
        today_provinces_data[it['name']]['children'] = today_cities_data

    provinces_json = os.path.join(SPIDER_DATA_DIRNAME, 'epidemic_domestic_data', 'province.json')
    provinces = json.load(open(provinces_json, 'r', encoding='utf-8'))

    today_date = dt.datetime.strptime(daily_data['data']['lastUpdateTime'].split(' ')[0], '%Y-%m-%d')
    time_delta = dt.timedelta(days=1)
    today_str = dt.datetime.strftime(today_date, '%Y-%m-%d')
    yesterday_str = dt.datetime.strftime(today_date - time_delta, '%Y-%m-%d')

    # 更新省数据
    # for province in province_dict_ch.keys():
    yesterday_provinces_data_list = []
    for it in provinces:
        if it['date'] == yesterday_str:
            yesterday_provinces_data_list = it['provinces']
    yesterday_provinces_data = {}
    for it in yesterday_provinces_data_list:
        yesterday_provinces_data[it['name']] = it
    today_data = []

    bar = tqdm(
        total=len(province_dict_ch), initial=0, dynamic_ncols=True,
    )

    for province in province_dict_ch.keys():
        bar.set_description('[updating province]')
        bar.update(1)
        bar.set_postfix_str(province)
        if province in yesterday_provinces_data.keys():
            cal_add = today_provinces_data[province]['total']['confirm'] - yesterday_provinces_data[province]['total'][
                'confirmed']
            real_add = today_provinces_data[province]['today']['confirm']
            if cal_add != real_add:
                print('%s新增人数有误' % province)
            today_data.append({
                'name': province,
                'new': {
                    'died': max(today_provinces_data[province]['total']['dead'] -
                                yesterday_provinces_data[province]['total']['died'], 0),
                    'cured': max(today_provinces_data[province]['total']['heal'] -
                                 yesterday_provinces_data[province]['total']['cured'], 0),
                    'confirmed': max(today_provinces_data[province]['total']['confirm'] -
                                     yesterday_provinces_data[province]['total']['confirmed'], 0),
                },
                'total': {
                    'died': today_provinces_data[province]['total']['dead'],
                    'cured': today_provinces_data[province]['total']['heal'],
                    'confirmed': today_provinces_data[province]['total']['confirm'],
                }
            })
        else:
            today_data.append({
                'name': province,
                'new': {
                    'died': 0,
                    'cured': 0,
                    'confirmed': 0,
                },
                'total': {
                    'died': yesterday_provinces_data[province]['total']['died'],
                    'cured': yesterday_provinces_data[province]['total']['cured'],
                    'confirmed': yesterday_provinces_data[province]['total']['confirmed'],
                }
            })
    find = False
    for idx in range(len(provinces)):
        if provinces[idx]['date'] == today_str:
            provinces[idx]['provinces'] = today_data
            find = True
    if not find:
        provinces.append({
            'date': today_str,
            'provinces': today_data
        })
    json.dump(provinces, open(provinces_json, 'w'), ensure_ascii=False)

    # 更新城市数据
    province_data_directory = os.path.join(SPIDER_DATA_DIRNAME, 'epidemic_domestic_data', 'provinces')

    bar = tqdm(
        total=len(province_dict_ch), initial=0, dynamic_ncols=True,
    )

    for province in province_dict_ch.keys():
        bar.set_description('[updating cities]')
        bar.update(1)
        bar.set_postfix_str(province)
        province_data = json.load(
            open(os.path.join(province_data_directory, '%s.json' % province_dict_ch[province]), 'r', encoding='utf-8'))
        yesterday_data_list = province_data[yesterday_str]
        yesterday_data = {}
        for it in yesterday_data_list:
            yesterday_data[it['name']] = it
        today_data = []
        for city_name, city in yesterday_data.items():
            for new_city_name, old_city_name in city_dict_ch.items():
                if old_city_name == city_name:
                    city_name = new_city_name
                    break
            today_cities_data = today_provinces_data[province]['children']
            if city_name in today_cities_data.keys():
                today_data.append({
                    'name': city_name,
                    'new': {
                        'died': max(today_cities_data[city_name]['total']['dead'] -
                                    city['total']['died'], 0),
                        'cured': max(today_cities_data[city_name]['total']['heal'] -
                                     city['total']['cured'], 0),
                        'confirmed': max(today_cities_data[city_name]['total']['confirm'] -
                                         city['total']['confirmed'], 0),
                    },
                    'total': {
                        'died': today_cities_data[city_name]['total']['dead'],
                        'cured': today_cities_data[city_name]['total']['heal'],
                        'confirmed': today_cities_data[city_name]['total']['confirm'],
                    }
                })
            else:
                today_data.append({
                    'name': city_name,
                    'new': {
                        'died': 0,
                        'cured': 0,
                        'confirmed': 0,
                    },
                    'total': {
                        'died': city['total']['died'],
                        'cured': city['total']['cured'],
                        'confirmed': city['total']['confirmed'],
                    }
                })

        province_data[today_str] = today_data
        json.dump(province_data,
                  open(os.path.join(province_data_directory,
                                    '%s.json' % province_dict_ch[province]), 'w', encoding='utf-8'), ensure_ascii=False)


if __name__ == '__main__':
    epidemic_domestic_daily_import()

'''
# print(province_data[0])
err_list = []
for old_city_name in city_dict_ch.keys():
    # for old_city_name in old_city.keys():
    find = False
    for it1 in province_data:
        province_name = it1['name']
        for it2 in it1['children']:
            city_name = it2['name']
            if '境外' in city_name:
                city_name += '-' + province_name
            if '外地' in city_name:
                city_name += '-' + province_name
            if '确认' in city_name:
                city_name += '-' + province_name
            if city_name in old_city_name:
                print(''%s': '%s',' % (city_name, old_city_name))
                find = True
            elif city_name in city_dict_ch[old_city_name]:
                print(''%s': '%s',' % (city_name, old_city_name))
                find = True
    if not find:
        err_list.append(old_city_name)
print(err_list)

print('{', end='')
for it2 in province_dict_ch.keys():
    find = False
    for it1 in province_data:
        if it1['name'] in it2:
            print(''%s': '%s',' % (it1['name'], it2))
            find = True
    if not find:
        print('error %s' % it2['name'])
print('}', end='')
'''
