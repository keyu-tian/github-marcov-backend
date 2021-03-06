city_dict_ch = {'东城区': '东城区', '西城区': '西城区', '朝阳区': '朝阳区', '丰台区': '丰台区', '石景山区': '石景山区', '海淀区': '海淀区', '门头沟区': '门头沟区',
                '房山区': '房山区', '通州区': '通州区', '顺义区': '顺义区', '昌平区': '昌平区', '大兴区': '大兴区', '怀柔区': '怀柔区', '密云区': '密云区',
                '延庆区': '延庆区', '万州区': '万州区', '涪陵区': '涪陵区', '渝中区': '渝中区', '大渡口区': '大渡口区', '江北区': '江北区', '沙坪坝区': '沙坪坝区',
                '九龙坡区': '九龙坡区', '南岸区': '南岸区', '綦江区': '綦江区', '大足区': '大足区', '渝北区': '渝北区', '巴南区': '巴南区', '黔江区': '黔江区',
                '长寿区': '长寿区', '江津区': '江津区', '合川区': '合川区', '永川区': '永川区', '璧山区': '璧山区', '铜梁区': '铜梁区', '潼南区': '潼南区',
                '荣昌区': '荣昌区', '城口县': '城口县', '丰都县': '丰都县', '垫江县': '垫江县', '忠县': '忠县', '云阳县': '云阳县', '奉节县': '奉节县',
                '巫山县': '巫山县', '巫溪县': '巫溪县', '开州区': '开州区', '金昌市': '金昌市', '白银市': '白银市', '天水市': '天水市', '平凉市': '平凉市',
                '河源市': '河源市', '琼海市': '琼海市', '东方市': '东方市', '澄迈县': '澄迈县', '临高县': '临高县', '邯郸市': '邯郸市', '安阳市': '安阳市',
                '鹤壁市': '鹤壁市', '漯河市': '漯河市', '神农架林区': '神农架林区', '吉林市': '吉林市', '四平市': '四平市', '抚顺市': '抚顺市',
                '包头市': '包头市昆都仑区', '乌海市': '乌海市', '赤峰市': '赤峰市松山区', '通辽市': '通辽市经济开发区', '呼伦贝尔市': '呼伦贝尔牙克石市', '兴安盟': '兴安盟',
                '锡林郭勒盟': '锡林郭勒盟', '西宁市': '西宁市', '淄博市': '淄博市', '黄浦区': '黄浦区', '徐汇区': '徐汇区', '长宁区': '长宁区', '静安区': '静安区',
                '普陀区': '普陀区', '虹口区': '虹口区', '杨浦区': '杨浦区', '闵行区': '闵行区', '宝山区': '宝山区', '嘉定区': '嘉定区', '浦东新区': '浦东新区',
                '金山区': '金山区', '松江区': '松江区', '青浦区': '青浦区', '奉贤区': '奉贤区', '崇明区': '崇明区', '朔州市': '朔州市', '临汾市': '临汾市',
                '和平区': '和平区', '河东区': '河东区', '河西区': '河西区', '南开区': '南开区', '河北区': '河北区', '红桥区': '红桥区', '东丽区': '东丽区',
                '西青区': '西青区', '津南区': '津南区', '北辰区': '北辰区', '武清区': '武清区', '宝坻区': '宝坻区', '滨海新区': '滨海新区', '宁河区': '宁河区',
                '吐鲁番市': '吐鲁番市', '阿克苏地区': '阿克苏地区', '喀什地区': '喀什地区', '石河子市': '兵团第八师石河子市', '五家渠市': '兵团第六师五家渠市',
                '丽江市': '丽江市', '中国属钓鱼岛': '中国属钓鱼岛', '兰州市': '兰州', '定西市': '定西', '甘南藏族自治州': '甘南', '陇南市': '陇南', '庆阳市': '庆阳',
                '临夏回族自治州': '临夏', '张掖市': '张掖', '福州市': '福州', '莆田市': '莆田', '泉州市': '泉州', '厦门市': '厦门', '宁德市': '宁德',
                '漳州市': '漳州', '南平市': '南平', '三明市': '三明', '龙岩市': '龙岩', '南宁市': '南宁', '北海市': '北海', '桂林市': '桂林', '河池市': '河池',
                '柳州市': '柳州', '防城港市': '防城港', '玉林市': '玉林', '来宾市': '来宾', '钦州市': '钦州', '贵港市': '贵港', '梧州市': '梧州',
                '贺州市': '贺州', '百色市': '百色', '德宏傣族景颇族自治州': '德宏州', '昆明市': '昆明', '昭通市': '昭通', '西双版纳傣族自治州': '西双版纳',
                '玉溪市': '玉溪', '曲靖市': '曲靖', '大理白族自治州': '大理州', '红河哈尼族彝族自治州': '红河州', '保山市': '保山', '普洱市': '普洱',
                '楚雄彝族自治州': '楚雄州', '文山壮族苗族自治州': '文山州', '临沧市': '临沧', '广州市': '广州', '深圳市': '深圳', '佛山市': '佛山', '珠海市': '珠海',
                '江门市': '江门', '东莞市': '东莞', '肇庆市': '肇庆', '阳江市': '阳江', '中山市': '中山', '惠州市': '惠州', '湛江市': '湛江', '汕头市': '汕头',
                '梅州市': '梅州', '茂名市': '茂名', '清远市': '清远', '揭阳市': '揭阳', '韶关市': '韶关', '潮州市': '潮州', '汕尾市': '汕尾', '成都市': '成都',
                '甘孜藏族自治州': '甘孜州', '达州市': '达州', '南充市': '南充', '广安市': '广安', '泸州市': '泸州', '巴中市': '巴中', '绵阳市': '绵阳',
                '内江市': '内江', '德阳市': '德阳', '遂宁市': '遂宁', '攀枝花市': '攀枝花', '凉山彝族自治州': '凉山州', '宜宾市': '宜宾', '自贡市': '自贡',
                '眉山市': '眉山', '雅安市': '雅安', '广元市': '广元', '资阳市': '资阳', '乐山市': '乐山', '阿坝藏族羌族自治州': '阿坝州', '大连市': '大连',
                '沈阳市': '沈阳', '锦州市': '锦州', '葫芦岛市': '葫芦岛', '丹东市': '丹东', '盘锦市': '盘锦', '营口市': '营口', '阜新市': '阜新',
                '铁岭市': '铁岭', '马鞍山市': '鞍山', '本溪市': '本溪', '辽阳市': '辽阳', '西安市': '西安', '安康市': '安康', '汉中市': '汉中', '咸阳市': '咸阳',
                '渭南市': '渭南', '宝鸡市': '宝鸡', '延安市': '延安', '铜川市': '铜川', '商洛市': '商洛', '榆林市': '榆林', '南京市': '南京', '苏州市': '苏州',
                '徐州市': '徐州', '淮安市': '淮安', '无锡市': '无锡', '常州市': '常州', '连云港市': '连云港', '南通市': '南通', '泰州市': '泰州',
                '盐城市': '盐城', '扬州市': '扬州', '宿迁市': '宿迁', '镇江市': '镇江', '长沙市': '长沙', '岳阳市': '岳阳', '邵阳市': '邵阳', '常德市': '常德',
                '株洲市': '株洲', '娄底市': '娄底', '益阳市': '益阳', '衡阳市': '衡阳', '永州市': '永州', '怀化市': '怀化', '郴州市': '郴州', '湘潭市': '湘潭',
                '湘西土家族苗族自治州': '湘西自治州', '张家界市': '张家界', '武汉市': '武汉', '孝感市': '孝感', '黄冈市': '黄冈', '荆州市': '荆州', '鄂州市': '鄂州',
                '随州市': '随州', '襄阳市': '襄阳', '黄石市': '黄石', '宜昌市': '宜昌', '荆门市': '荆门', '咸宁市': '咸宁', '十堰市': '十堰', '仙桃市': '仙桃',
                '天门市': '天门', '恩施土家族苗族自治州': '恩施州', '潜江市': '潜江', '合肥市': '合肥', '蚌埠市': '蚌埠', '阜阳市': '阜阳', '亳州市': '亳州',
                '安庆市': '安庆', '六安市': '六安', '宿州市': '宿州', '芜湖市': '芜湖', '铜陵市': '铜陵', '淮北市': '淮北', '淮南市': '淮南', '池州市': '池州',
                '滁州市': '滁州', '黄山市': '黄山', '宣城市': '宣城', '济宁市': '济宁', '青岛市': '青岛', '临沂市': '临沂', '济南市': '济南', '烟台市': '烟台',
                '潍坊市': '潍坊', '威海市': '威海', '聊城市': '聊城', '德州市': '德州', '泰安市': '泰安', '枣庄市': '枣庄', '菏泽市': '菏泽', '日照市': '日照',
                '滨州市': '滨州', '鄂尔多斯市': '鄂尔多斯', '巴彦淖尔市': '巴彦淖尔', '呼和浩特市': '呼和浩特', '乌兰察布市': '乌兰察布', '温州市': '温州',
                '杭州市': '杭州', '宁波市': '宁波', '台州市': '台州', '金华市': '金华', '嘉兴市': '嘉兴', '绍兴市': '绍兴', '丽水市': '丽水', '衢州市': '衢州',
                '湖州市': '湖州', '舟山市': '舟山', '信阳市': '信阳', '郑州市': '郑州', '南阳市': '南阳', '驻马店市': '驻马店', '商丘市': '商丘',
                '周口市': '周口', '平顶山市': '平顶山', '新乡市': '新乡', '许昌市': '许昌', '焦作市': '焦作', '洛阳市': '洛阳', '开封市': '开封',
                '濮阳市': '濮阳', '三门峡市': '三门峡', '济源市': '济源', '石柱土家族自治县': '石柱县', '彭水苗族土家族自治县': '彭水县', '秀山土家族苗族自治县': '秀山县',
                '酉阳土家族苗族自治县': '酉阳县', '晋中市': '晋中', '太原市': '太原', '运城市': '运城', '大同市': '大同', '晋城市': '晋城', '长治市': '长治',
                '忻州市': '忻州', '吕梁市': '吕梁', '阳泉市': '阳泉', '绥化市': '绥化', '哈尔滨市': '哈尔滨', '双鸭山市': '双鸭山', '鸡西市': '鸡西',
                '齐齐哈尔市': '齐齐哈尔', '牡丹江市': '牡丹江', '大庆市': '大庆', '黑河市': '黑河', '七台河市': '七台河', '佳木斯市': '佳木斯', '鹤岗市': '鹤岗',
                '大兴安岭地区': '大兴安岭', '伊春市': '伊春', '三亚市': '三亚', '海口市': '海口', '儋州市': '儋州', '万宁市': '万宁', '昌江黎族自治县': '昌江',
                '陵水黎族自治县': '陵水', '定安县': '定安', '文昌市': '文昌', '保亭黎族苗族自治县': '保亭', '乐东黎族自治县': '乐东', '琼中黎族苗族自治县': '琼中',
                '银川市': '银川', '吴忠市': '吴忠', '固原市': '固原', '中卫市': '中卫', '石嘴山市': '石嘴山', '保定市': '保定', '石家庄市': '石家庄',
                '邢台市': '邢台', '唐山市': '唐山', '沧州市': '沧州', '张家口市': '张家口', '廊坊市': '廊坊', '秦皇岛市': '秦皇岛', '衡水市': '衡水',
                '承德市': '承德', '海北藏族自治州': '海北州', '南昌市': '南昌', '新余市': '新余', '上饶市': '上饶', '九江市': '九江', '宜春市': '宜春',
                '赣州市': '赣州', '抚州市': '抚州', '萍乡市': '萍乡', '吉安市': '吉安', '鹰潭市': '鹰潭', '景德镇市': '景德镇', '通化市': '通化',
                '长春市': '长春', '辽源市': '辽源', '延边朝鲜族自治州': '延边', '松原市': '松原', '白城市': '白城', '拉萨市': '拉萨', '乌鲁木齐市': '乌鲁木齐',
                '伊犁哈萨克自治州': '伊犁州', '昌吉回族自治州': '昌吉州', '巴音郭楞蒙古自治州': '巴州', '贵阳市': '贵阳', '遵义市': '遵义', '毕节市': '毕节',
                '黔西南布依族苗族自治州': '黔南州', '六盘水市': '六盘水', '铜仁市': '铜仁', '黔东南苗族侗族自治州': '黔东南州', '安顺市': '安顺', '塔城地区': '塔城'}
province_dict_ch = {'安徽': '安徽省', '北京': '北京市', '重庆': '重庆市', '福建': '福建省', '甘肃': '甘肃省', '广东': '广东省', '广西': '广西壮族自治区',
                    '贵州': '贵州省', '海南': '海南省', '河北': '河北省', '黑龙江': '黑龙江省', '河南': '河南省', '湖北': '湖北省', '湖南': '湖南省',
                    '江苏': '江苏省', '江西': '江西省', '吉林': '吉林省', '辽宁': '辽宁省', '内蒙古': '内蒙古自治区', '宁夏': '宁夏回族自治区', '青海': '青海省',
                    '山东': '山东省', '上海': '上海市', '山西': '山西省', '陕西': '陕西省', '四川': '四川省', '台湾': '台湾', '天津': '天津市',
                    '新疆': '新疆维吾尔自治区', '西藏': '西藏自治区', '云南': '云南省', '浙江': '浙江省', '香港': '香港', '澳门': '澳门'}
province_population = {
    '北京': 21893095,
    '天津': 13866009,
    '河北': 74610235,
    '山西': 34915616,
    '内蒙古': 24049155,
    '辽宁': 42591407,
    '吉林': 24073453,
    '黑龙江': 31850088,
    '上海': 24870895,
    '江苏': 84748016,
    '浙江': 64567588,
    '安徽': 61027171,
    '福建': 41540086,
    '江西': 45188635,
    '山东': 101527453,
    '河南': 99365519,
    '湖北': 57752557,
    '湖南': 66444864,
    '广东': 126012510,
    '广西': 50126804,
    '海南': 10081232,
    '重庆': 32054159,
    '四川': 83674866,
    '贵州': 38562148,
    '云南': 47209277,
    '西藏': 3648100,
    '陕西': 39528999,
    '甘肃': 25019831,
    '青海': 5923957,
    '宁夏': 7202654,
    '新疆': 25852345,
    '香港': 7547652,
    '澳门': 676100,
    '台湾': 23817905
}



