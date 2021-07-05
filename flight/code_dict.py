code_dict = {
    "阿勒泰": "AAT", "阿克苏": "AKU", "鞍山": "AOG", "安庆": "AQG", "安顺": "AVA", "阿拉善左旗": "AXF", "澳门": "MFM", "阿里": "NGQ",
    "阿拉善右旗": "RHT", "阿尔山": "YIE", "巴中": "BZX", "百色": "AEB", "包头": "BAV", "毕节": "BFJ", "北海": "BHY", "北京": "BJS",
    "北京(南苑机场)": "NAY", "北京(首都国际机场)": "PEK", "博乐": "BPL", "保山": "BSD", "白城": "DBC", "布尔津": "KJI", "白山": "NBS",
    "巴彦淖尔": "RLK", "昌都": "BPX", "承德": "CDE", "常德": "CGD", "长春": "CGQ", "朝阳": "CHG", "赤峰": "CIF", "长治": "CIH",
    "重庆": "CKG", "长沙": "CSX", "成都": "CTU", "沧源": "CWJ", "常州": "CZX", "池州": "JUH", "潮州": "SWA", "潮汕": "SWA",
    "大同": "DAT", "达县": "DAX", "达州": "DAX", "稻城": "DCY", "丹东": "DDG", "迪庆": "DIG", "大连": "DLC", "大理": "DLU",
    "敦煌": "DNH", "东营": "DOY", "大庆": "DQA", "德令哈": "HXD", "德宏": "LUM", "鄂尔多斯": "DSN", "额济纳旗": "EJN", "恩施": "ENH",
    "二连浩特": "ERL", "福州": "FOC", "阜阳": "FUG", "抚远": "FYJ", "富蕴": "FYN",
    "广州": "CAN", "果洛": "GMQ", "格尔木": "GOQ", "广元": "GYS", "固原": "GYU", "高雄": "KHH", "赣州": "KOW", "贵阳": "KWE",
    "桂林": "KWL", "红原": "AHJ", "海口": "HAK", "河池": "HCJ", "邯郸": "HDG", "黑河": "HEK", "呼和浩特": "HET", "合肥": "HFE",
    "杭州": "HGH", "淮安": "HIA", "怀化": "HJJ", "海拉尔": "HLD", "哈密": "HMI", "衡阳": "HNY", "哈尔滨": "HRB", "和田": "HTN",
    "花土沟": "HTT", "花莲": "HUN", "霍林郭勒": "HUO", "惠阳": "HUZ", "惠州": "HUZ", "汉中": "HZG", "黄山": "TXN", "呼伦贝尔": "XRQ",
    "嘉义": "CYI", "景德镇": "JDZ", "加格达奇": "JGD", "嘉峪关": "JGN", "井冈山": "JGS", "景洪": "JHG", "金昌": "JIC", "九江": "JIU",
    "晋江": "JJN", "荆门": "JM1", "佳木斯": "JMU", "济宁": "JNG", "锦州": "JNZ", "建三江": "JSJ", "鸡西": "JXA", "九寨沟": "JZH",
    "金门": "KNH", "揭阳": "SWA", "济南": "TNA",
    "库车": "KCA", "康定": "KGT", "喀什": "KHG", "凯里": "KJH", "昆明": "KMG", "库尔勒": "KRL", "克拉玛依": "KRY", "黎平": "HZH",
    "澜沧": "JMJ", "连城": "LCX", "龙岩": "LCX", "临汾": "LFQ", "兰州": "LHW", "丽江": "LJG", "荔波": "LLB", "吕梁": "LLV",
    "临沧": "LNJ", "陇南": "LNL", "六盘水": "LPF", "拉萨": "LXA", "洛阳": "LYA", "连云港": "LYG", "临沂": "LYI", "柳州": "LZH",
    "泸州": "LZO", "林芝": "LZY", "芒市": "LUM", "牡丹江": "MDG", "马祖": "MFK", "绵阳": "MIG", "梅县": "MXZ", "梅州": "MXZ",
    "马公": "MZG", "满洲里": "NZH", "漠河": "OHE", "南昌": "KHN", "南竿": "LZN", "南充": "NAO", "宁波": "NGB", "南京": "NKG",
    "宁蒗": "NLH", "南宁": "NNG", "南阳": "NNY", "南通": "NTG",
    "澎湖列岛": "MZG", "攀枝花": "PZI", "普洱": "SYM", "琼海": "BAR", "秦皇岛": "BPE", "祁连": "HBQ", "且末": "IQM", "庆阳": "IQN",
    "黔江": "JIQ", "泉州": "JJN", "衢州": "JUZ", "齐齐哈尔": "NDG", "青岛": "TAO", "日照": "RIZ", "日喀则": "RKZ", "若羌": "RQA",
    "神农架": "HPG", "石狮": "JJN", "莎车": "QSZ", "上海": "SHA", "上海(浦东国际机场)": "PVG", "上海(虹桥国际机场)": "SHA", "沈阳": "SHE",
    "石河子": "SHF", "石家庄": "SJW", "上饶": "SQD", "三明": "SQJ", "汕头": "SWA", "三亚": "SYX", "深圳": "SZX", "十堰": "WDS",
    "邵阳": "WGN", "松原": "YSQ", "台州": "HYN", "台中": "RMQ", "塔城": "TCG", "腾冲": "TCZ", "铜仁": "TEN", "通辽": "TGO",
    "天水": "THQ", "吐鲁番": "TLQ", "通化": "TNH", "台南": "TNN", "台北": "TPE", "天津": "TSN", "台东": "TTT", "唐山": "TVS",
    "太原": "TYN", "泰州": "YTY", "五大连池": "DTU", "乌兰浩特": "HLH", "乌兰察布": "UCB", "乌鲁木齐": "URC", "潍坊": "WEF", "威海": "WEH",
    "文山": "WNH", "温州": "WNZ", "乌海": "WUA", "武汉": "WUH", "武夷山": "WUS", "无锡": "WUX", "梧州": "WUZ", "万州": "WXN",
    "乌拉特中旗": "WZQ",
    "兴义": "ACX", "香格里拉": "DIG", "夏河": "GXH", "香港": "HKG", "西双版纳": "JHG", "新源": "NLT", "西安": "SIA", "咸阳": "SIA",
    "忻州": "WUT", "信阳": "XAI", "襄阳": "XFN", "西昌": "XIC", "锡林浩特": "XIL", "厦门": "XMN", "西宁": "XNN", "徐州": "XUZ",
    "延安": "ENY", "银川": "INC", "伊春": "LDS", "永州": "LLF", "榆林": "UYN", "宜宾": "YBP", "运城": "YCU", "宜春": "YIC",
    "宜昌": "YIH", "伊犁": "YIN", "伊宁": "YIN", "义乌": "YIW", "营口": "YKH", "延吉": "YNJ", "烟台": "YNT", "盐城": "YNZ",
    "扬州": "YTY", "玉树": "YUS", "岳阳": "YYA", "郑州": "CGO", "张家界": "DYG", "芷江": "HJJ", "舟山": "HSN", "扎兰屯": "NZL",
    "张掖": "YZY", "昭通": "ZAT", "湛江": "ZHA", "中卫": "ZHY", "张家口": "ZQZ", "珠海": "ZUH", "遵义": "ZYI",
}

inverse_dic = {{'AAT': '阿勒泰', 'AKU': '阿克苏', 'AOG': '鞍山', 'AQG': '安庆', 'AVA': '安顺', 'AXF': '阿拉善左旗',
                'MFM': '澳门', 'NGQ': '阿里', 'RHT': '阿拉善右旗', 'YIE': '阿尔山', 'BZX': '巴中', 'AEB': '百色',
                'BAV': '包头', 'BFJ': '毕节', 'BHY': '北海', 'BJS': '北京', 'NAY': '北京',
                'PEK': '北京', 'BPL': '博乐', 'BSD': '保山', 'DBC': '白城', 'KJI': '布尔津',
                'NBS': '白山', 'RLK': '巴彦淖尔', 'BPX': '昌都', 'CDE': '承德', 'CGD': '常德', 'CGQ': '长春',
                'CHG': '朝阳', 'CIF': '赤峰', 'CIH': '长治', 'CKG': '重庆', 'CSX': '长沙', 'CTU': '成都',
                'CWJ': '沧源', 'CZX': '常州', 'JUH': '池州', 'SWA': '汕头', 'DAT': '大同', 'DAX': '达州',
                'DCY': '稻城', 'DDG': '丹东', 'DIG': '香格里拉', 'DLC': '大连', 'DLU': '大理', 'DNH': '敦煌',
                'DOY': '东营', 'DQA': '大庆', 'HXD': '德令哈', 'LUM': '芒市', 'DSN': '鄂尔多斯', 'EJN': '额济纳旗',
                'ENH': '恩施', 'ERL': '二连浩特', 'FOC': '福州', 'FUG': '阜阳', 'FYJ': '抚远', 'FYN': '富蕴',
                'CAN': '广州', 'GMQ': '果洛', 'GOQ': '格尔木', 'GYS': '广元', 'GYU': '固原', 'KHH': '高雄',
                'KOW': '赣州', 'KWE': '贵阳', 'KWL': '桂林', 'AHJ': '红原', 'HAK': '海口', 'HCJ': '河池',
                'HDG': '邯郸', 'HEK': '黑河', 'HET': '呼和浩特', 'HFE': '合肥', 'HGH': '杭州', 'HIA': '淮安',
                'HJJ': '芷江', 'HLD': '海拉尔', 'HMI': '哈密', 'HNY': '衡阳', 'HRB': '哈尔滨', 'HTN': '和田',
                'HTT': '花土沟', 'HUN': '花莲', 'HUO': '霍林郭勒', 'HUZ': '惠州', 'HZG': '汉中', 'TXN': '黄山',
                'XRQ': '呼伦贝尔', 'CYI': '嘉义', 'JDZ': '景德镇', 'JGD': '加格达奇', 'JGN': '嘉峪关',
                'JGS': '井冈山', 'JHG': '西双版纳', 'JIC': '金昌', 'JIU': '九江', 'JJN': '石狮', 'JM1': '荆门',
                'JMU': '佳木斯', 'JNG': '济宁', 'JNZ': '锦州', 'JSJ': '建三江', 'JXA': '鸡西', 'JZH': '九寨沟',
                'KNH': '金门', 'TNA': '济南', 'KCA': '库车', 'KGT': '康定', 'KHG': '喀什', 'KJH': '凯里',
                'KMG': '昆明', 'KRL': '库尔勒', 'KRY': '克拉玛依', 'HZH': '黎平', 'JMJ': '澜沧', 'LCX': '龙岩',
                'LFQ': '临汾', 'LHW': '兰州', 'LJG': '丽江', 'LLB': '荔波', 'LLV': '吕梁', 'LNJ': '临沧',
                'LNL': '陇南', 'LPF': '六盘水', 'LXA': '拉萨', 'LYA': '洛阳', 'LYG': '连云港', 'LYI': '临沂',
                'LZH': '柳州', 'LZO': '泸州', 'LZY': '林芝', 'MDG': '牡丹江', 'MFK': '马祖', 'MIG': '绵阳',
                'MXZ': '梅州', 'MZG': '澎湖列岛', 'NZH': '满洲里', 'OHE': '漠河', 'KHN': '南昌', 'LZN': '南竿',
                'NAO': '南充', 'NGB': '宁波', 'NKG': '南京', 'NLH': '宁蒗', 'NNG': '南宁', 'NNY': '南阳',
                'NTG': '南通', 'PZI': '攀枝花', 'SYM': '普洱', 'BAR': '琼海', 'BPE': '秦皇岛', 'HBQ': '祁连',
                'IQM': '且末', 'IQN': '庆阳', 'JIQ': '黔江', 'JUZ': '衢州', 'NDG': '齐齐哈尔', 'TAO': '青岛',
                'RIZ': '日照', 'RKZ': '日喀则', 'RQA': '若羌', 'HPG': '神农架', 'QSZ': '莎车',
                'SHA': '上海', 'PVG': '上海', 'SHE': '沈阳', 'SHF': '石河子',
                'SJW': '石家庄', 'SQD': '上饶', 'SQJ': '三明', 'SYX': '三亚', 'SZX': '深圳', 'WDS': '十堰',
                'WGN': '邵阳', 'YSQ': '松原', 'HYN': '台州', 'RMQ': '台中', 'TCG': '塔城', 'TCZ': '腾冲',
                'TEN': '铜仁', 'TGO': '通辽', 'THQ': '天水', 'TLQ': '吐鲁番', 'TNH': '通化', 'TNN': '台南',
                'TPE': '台北', 'TSN': '天津', 'TTT': '台东', 'TVS': '唐山', 'TYN': '太原', 'YTY': '扬州',
                'DTU': '五大连池', 'HLH': '乌兰浩特', 'UCB': '乌兰察布', 'URC': '乌鲁木齐', 'WEF': '潍坊',
                'WEH': '威海', 'WNH': '文山', 'WNZ': '温州', 'WUA': '乌海', 'WUH': '武汉', 'WUS': '武夷山',
                'WUX': '无锡', 'WUZ': '梧州', 'WXN': '万州', 'WZQ': '乌拉特中旗', 'ACX': '兴义', 'GXH': '夏河',
                'HKG': '香港', 'NLT': '新源', 'SIA': '咸阳', 'WUT': '忻州', 'XAI': '信阳', 'XFN': '襄阳',
                'XIC': '西昌', 'XIL': '锡林浩特', 'XMN': '厦门', 'XNN': '西宁', 'XUZ': '徐州', 'ENY': '延安',
                'INC': '银川', 'LDS': '伊春', 'LLF': '永州', 'UYN': '榆林', 'YBP': '宜宾', 'YCU': '运城',
                'YIC': '宜春', 'YIH': '宜昌', 'YIN': '伊宁', 'YIW': '义乌', 'YKH': '营口', 'YNJ': '延吉',
                'YNT': '烟台', 'YNZ': '盐城', 'YUS': '玉树', 'YYA': '岳阳', 'CGO': '郑州', 'DYG': '张家界',
                'HSN': '舟山', 'NZL': '扎兰屯', 'YZY': '张掖', 'ZAT': '昭通', 'ZHA': '湛江', 'ZHY': '中卫',
                'ZQZ': '张家口', 'ZUH': '珠海', 'ZYI': '遵义'}
               }
