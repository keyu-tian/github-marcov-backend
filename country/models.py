import json
import re

from django.db import models

from utils.cast import gd_address_to_jingwei_and_province_city
from utils.dict_ch import province_dict_ch
from utils.locatable_cities import locatable_cities


class Country(models.Model):
    @staticmethod
    def standardize_name(name):
        return name.strip()
    
    @staticmethod
    def get_via_name(not_standard_name):
        q = Country.objects.filter(name_ch=Country.standardize_name(not_standard_name))
        if q.exists():
            return q.get()
        return None
    
    name_ch = models.CharField(primary_key=True, unique=True, db_index=True, max_length=128, blank=True)
    name_en = models.CharField(max_length=512, blank=True)


class Province(models.Model):
    @staticmethod
    def standardize_name(name):
        return province_dict_ch.get(re.sub('市|直辖市|省|地区', '', name.strip()).strip(), None)
    
    @staticmethod
    def get_via_name(not_standard_name):
        q = Province.objects.filter(name_ch=Province.standardize_name(not_standard_name))
        if q.exists():
            return q.get()
        return None
    
    name_ch = models.CharField(primary_key=True, unique=True, db_index=True, max_length=128, blank=True)
    name_en = models.CharField(max_length=512, blank=True)
    country = models.ForeignKey(to=Country, on_delete=models.CASCADE, related_name='province_set', blank=True, null=True)


class City(models.Model):
    @staticmethod
    def standardize_name(name):
        info = locatable_cities.get(re.sub('市|直辖市|县|地区', '', name.strip()).strip(), None)
        return None if info is None else info[3]
    
    @staticmethod
    def get_via_name(not_standard_name):
        q = City.objects.filter(name_ch=City.standardize_name(not_standard_name))
        if q.exists():
            return q.get()
        return None
    
    name_ch = models.CharField(primary_key=True, unique=True, db_index=True, max_length=128, blank=True)
    name_en = models.CharField(max_length=512, blank=True)
    province = models.ForeignKey(to=Province, on_delete=models.CASCADE, related_name='province_city_set', blank=True, null=True)
    country = models.ForeignKey(to=Country, on_delete=models.CASCADE, related_name='country_city_set', blank=True, null=True)
    jingdu = models.FloatField(blank=True, null=True)
    weidu = models.FloatField(blank=True, null=True)


class Policy(models.Model):
    city = models.ForeignKey(to=City, on_delete=models.DO_NOTHING, related_name='policy_set', blank=True, null=True)
    province = models.ForeignKey(to=Province, on_delete=models.DO_NOTHING, related_name='policy_set', blank=True, null=True)
    city_name = models.CharField(max_length=128, blank=True, null=True)
    province_name = models.CharField(max_length=128, blank=True, null=True)
    enter_policy = models.TextField(blank=True, null=True)
    out_policy = models.TextField(blank=True, null=True)


# def get_locatable_cities():
#     wz_set = {'连城', '中卫', '韶关', '海拉尔', '温州', '九寨沟', '襄樊', '马公', '达县', '酒泉', '昆明', '杭州', '常州', '腾冲', '阿勒泰', '保山', '烟台', '武夷山', '十堰', '百色', '台中', '怀化', '拉萨', '大理', '张家界', '泉州', '珠海', '朝阳', '上饶', '锡林浩特',
#               '遵义', '鄂尔多斯', '屏东', '哈密', '塔城', '台湾', '大足', '汕头', '香港', '池州', '阿克苏', '临沂', '衢州', '库车', '阿坝', '宁波', '蚌埠', '阜阳', '昭通', '林西', '黔江', '武冈', '汉中', '桂林', '长白山', '万州', '长治', '阿尔山', '安阳', '苏州',
#               '惠州', '兴义', '无锡', '漠河', '绵阳', '三亚', '大连', '嘉义', '新竹', '赣州', '深圳', '唐山', '沙市', '安庆', '郑州', '齐齐哈尔', '恩施', '景德镇', '西宁', '安康', '乌海', '广州', '呼和浩特', '黄岩', '长沙', '哈尔滨', '庆阳', '常德', '博乐', '台东',
#               '包头', '临沧', '南充', '银川', '吉林', '宜昌', '潍坊', '巴中', '大庆', '赤峰', '膳善', '福州', '乌鲁木齐', '澳门', '重庆', '松原', '神农架', '佳木斯', '南竿', '库尔勒', '大同', '北京南苑', '兰屿', '高雄', '西昌', '石家庄', '二连浩特', '天津', '衡阳',
#               '沈阳', '成都', '湛江', '梅县', '锦州', '牡丹江', '南京', '攀枝花', '九江', '富蕴', '东莞', '临汾', '威海', '台北', '井冈山', '林芝', '黑河', '立山', '合肥', '邯郸', '长春', '青岛', '金昌市', '厦门', '鞍山', '南通', '南阳', '贵阳', '和田', '济南',
#               '金门', '且末', '通辽', '连云港', '乌兰浩特', '太原', '丽江', '广汉', '泸州', '武汉', '通化', '洛阳', '嘉峪关', '淮安', '南昌', '迪庆', '梧州', '徐州', '安顺', '敦煌', '柳州', '丹东', '芒市', '固原', '天水', '昌都', '台南', '宜春', '喀什', '上海',
#               '海口', '七美', '玉树', '宜宾', '南宁', '广元', '兰州', '黎平', '邢台', '济宁', '北海', '加格达奇', '东营', '黄山', '舟山', '阿里地区狮泉河镇', '思茅', '马祖', '西安', '西双版纳', '秦皇岛', '克拉玛依', '北京', '格尔木', '佛山', '长海'}
#     for city in wz_set:
#         res = gd_address_to_jingwei_and_province_city(city)
#         if res is not None:
#             City.objects.get_or_create(
#                 name_ch=city, defaults=dict(
#                     name_en='', jingdu=res['jingdu'], weidu=res['weidu'],
#                     country=Country.objects.get(name_ch='中国')
#                 )
#             )
#
#     all_citys = set([re.sub('市|直辖市|县|地区', '', t[0].strip()).strip() for t in City.objects.values_list('name_ch')])
#     dd = {}
#     for x in all_citys:
#         res = gd_address_to_jingwei_and_province_city(x)
#         if res is not None:
#             dd[x] = [res['jingdu'], res['weidu'], res['district'], res['city'], res['province'], res['country']]
#     with open('locatable_cities.json', 'w') as fp:
#         json.dump(dd, fp, indent=2, ensure_ascii=False)
#     return dd
