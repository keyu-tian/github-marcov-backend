country_dict = {
    "South Sudan": "南苏丹",
    "Qatar": "卡塔尔",
    "Laos": "老挝",
    "Philippines": "菲律宾",
    "South Africa": "南非",
    "Albania": "阿尔巴尼亚",
    "Russia": "俄罗斯",
    "Chile": "智利",
    "Andorra": "安道尔",
    "New Zealand": "新西兰",
    "Sudan": "苏丹",
    "Iran": "伊朗",
    "Afghanistan": "阿富汗",
    "Monaco": "摩纳哥",
    "Samoa": "萨摩亚",
    "Malta": "马耳他",
    "Suriname": "苏里南",
    "United Arab Emirates": "阿拉伯联合酋长国",
    "Tajikistan": "塔吉克斯坦",
    "Central African Republic": "中非共和国",
    "France": "法国",
    "Zambia": "赞比亚",
    "Bosnia and Herzegovina": "波斯尼亚-黑塞哥维那",
    "US": "美国",
    "Djibouti": "吉布提",
    "Oman": "阿曼",
    "Syria": "叙利亚",
    "Egypt": "埃及",
    "Kenya": "肯尼亚",
    "Ghana": "加纳",
    "Slovenia": "斯洛文尼亚",
    "Tunisia": "突尼斯",
    "Vanuatu": "瓦努阿图",
    "Bulgaria": "保加利亚",
    "Palau": "帕劳",
    "Lebanon": "黎巴嫩",
    "Nepal": "尼泊尔",
    "Somalia": "索马里",
    "Georgia": "格鲁吉亚",
    "Finland": "芬兰",
    "Greece": "希腊",
    "Burundi": "蒲隆地",
    "Jamaica": "牙买加",
    "Mongolia": "蒙古",
    "Uganda": "乌干达",
    "Zimbabwe": "津巴布韦",
    "Brunei": "文莱",
    "Papua New Guinea": "巴布亚新几内亚",
    "Marshall Islands": "马绍尔群岛",
    "Thailand": "泰国",
    "Guatemala": "危地马拉",
    "Mexico": "墨西哥",
    "Namibia": "纳米比亚",
    "Bangladesh": "孟加拉国",
    "El Salvador": "萨尔瓦多",
    "Venezuela": "委内瑞拉",
    "Solomon Islands": "所罗门群岛",
    "Burkina Faso": "布基纳法索",
    "Trinidad and Tobago": "特立尼达和多巴哥",
    "Cuba": "古巴",
    "Sri Lanka": "斯里兰卡",
    "Guinea": "几内亚",
    "Eritrea": "厄立特里亚",
    "Armenia": "亚美尼亚",
    "Angola": "安哥拉",
    "Saint Vincent and the Grenadines": "圣文森特和格林纳丁斯",
    "Cameroon": "喀麦隆",
    "India": "印度",
    "Kosovo": "科索沃",
    "Portugal": "葡萄牙",
    "Slovakia": "斯洛伐克",
    "Colombia": "哥伦比亚",
    "Nigeria": "尼日利亚",
    "Liechtenstein": "列支敦士登",
    "Niger": "尼日尔",
    "Paraguay": "巴拉圭",
    "Equatorial Guinea": "赤道几内亚",
    "Saint Lucia": "圣卢西亚",
    "Mozambique": "莫桑比克",
    "Saint Kitts and Nevis": "圣基茨和尼维斯",
    "Iraq": "伊拉克",
    "Seychelles": "塞舌尔",
    "Tanzania": "坦桑尼亚",
    "Bahamas": "巴哈马",
    "Malaysia": "马来西亚",
    "Peru": "秘鲁",
    "Ukraine": "乌克兰",
    "Vietnam": "越南",
    "Azerbaijan": "阿塞拜疆",
    "Sweden": "瑞典",
    "Dominica": "多米尼克",
    "Gambia": "冈比亚",
    "Bhutan": "不丹",
    "Libya": "利比亚",
    "Indonesia": "印度尼西亚, 印尼",
    "Jordan": "约旦",
    "Madagascar": "马达加斯加",
    "Moldova": "摩尔多瓦",
    "Saudi Arabia": "沙特阿拉伯",
    "Ecuador": "厄瓜多尔",
    "Antigua and Barbuda": "安提瓜和巴布达",
    "Cyprus": "塞浦路斯",
    "Estonia": "爱沙尼亚",
    "Comoros": "科摩罗",
    "Fiji": "斐济",
    "Spain": "西班牙",
    "Botswana": "博茨瓦纳",
    "Austria": "奥地利",
    "Togo": "多哥",
    "Mali": "马里",
    "Ethiopia": "埃塞俄比亚",
    "Romania": "罗马尼亚",
    "Uzbekistan": "乌兹别克斯坦",
    "Bahrain": "巴林",
    "Algeria": "阿尔及利亚",
    "Honduras": "洪都拉斯",
    "Belize": "伯利兹",
    "Japan": "日本",
    "Kyrgyzstan": "吉尔吉斯斯坦",
    "Korea, South": "韩国",
    "Hungary": "匈牙利",
    "Mauritius": "毛里求斯",
    "Haiti": "海地",
    "Czechia": "捷克",
    "Cambodia": "柬埔寨",
    "Kiribati": "基里巴斯",
    "Uruguay": "乌拉圭",
    "San Marino": "圣马力诺",
    "Poland": "波兰",
    "Liberia": "利比里亚",
    "Kazakhstan": "哈萨克斯坦",
    "Canada": "加拿大",
    "Belarus": "白俄罗斯",
    "China": "中国",
    "Costa Rica": "哥斯达黎加",
    "Sierra Leone": "塞拉利昂",
    "Latvia": "拉脱维亚",
    "Australia": "澳大利亚",
    "Serbia": "塞尔维亚",
    "Morocco": "摩洛哥",
    "Senegal": "塞内加尔",
    "Chad": "乍得",
    "Italy": "意大利",
    "Ireland": "爱尔兰",
    "United Kingdom": "英国",
    "Singapore": "新加坡",
    "Croatia": "克罗地亚",
    "Benin": "贝宁",
    "Montenegro": "黑山",
    "Yemen": "也门",
    "Mauritania": "毛里塔尼亚",
    "Norway": "挪威",
    "Pakistan": "巴基斯坦",
    "Turkey": "土耳其",
    "Lithuania": "立陶宛",
    "Argentina": "阿根廷",
    "Netherlands": "荷兰",
    "Gabon": "加蓬",
    "Switzerland": "瑞士",
    "Rwanda": "卢旺达",
    "Belgium": "比利时",
    "Panama": "巴拿马",
    "Malawi": "马拉维",
    "Bolivia": "玻利维亚",
    "Guyana": "圭亚那",
    "Barbados": "巴巴多斯",
    "Lesotho": "莱索托",
    "Brazil": "巴西",
    "Maldives": "马尔代夫",
    "Israel": "以色列",
    "Dominican Republic": "多米尼加共和国",
    "Guinea-Bissau": "几内亚比索",
    "Germany": "德国",
    "Kuwait": "科威特",
    "Denmark": "丹麦",
    "Iceland": "冰岛",
    "Nicaragua": "尼加拉瓜"
}

country_population = {'China': 1439323776, 'India': 1380004385, 'US': 331002651, 'Indonesia': 273523615,
                      'Pakistan': 220892340, 'Brazil': 212559417, 'Nigeria': 206139589, 'Bangladesh': 164689383,
                      'Russia': 145934462, 'Mexico': 128932753, 'Japan': 126476461, 'Ethiopia': 114963588,
                      'Philippines': 109581078, 'Egypt': 102334404, 'Vietnam': 97338579, 'Turkey': 84339067,
                      'Iran': 83992949, 'Germany': 83783942, 'Thailand': 69799978, 'United Kingdom': 67886011,
                      'France': 65273511, 'Italy': 60461826, 'Tanzania': 59734218, 'South Africa': 59308690,
                      'Kenya': 53771296, 'Colombia': 50882891, 'Spain': 46754778, 'Uganda': 45741007,
                      'Argentina': 45195774, 'Algeria': 43851044, 'Sudan': 43849260, 'Ukraine': 43733762,
                      'Iraq': 40222493, 'Afghanistan': 38928346, 'Poland': 37846611, 'Canada': 37742154,
                      'Morocco': 36910560, 'Saudi Arabia': 34813871, 'Uzbekistan': 33469203, 'Peru': 32971854,
                      'Angola': 32866272, 'Malaysia': 32365999, 'Mozambique': 31255435, 'Ghana': 31072940,
                      'Yemen': 29825964, 'Nepal': 29136808, 'Venezuela': 28435940, 'Madagascar': 27691018,
                      'Cameroon': 26545863, 'Australia': 25499884, 'Niger': 24206644, 'Sri Lanka': 21413249,
                      'Burkina Faso': 20903273, 'Mali': 20250833, 'Romania': 19237691, 'Malawi': 19129952,
                      'Chile': 19116201, 'Kazakhstan': 18776707, 'Zambia': 18383955, 'Guatemala': 17915568,
                      'Ecuador': 17643054, 'Syria': 17500658, 'Netherlands': 17134872, 'Senegal': 16743927,
                      'Cambodia': 16718965, 'Chad': 16425864, 'Somalia': 15893222, 'Zimbabwe': 14862924,
                      'Guinea': 13132795, 'Rwanda': 12952218, 'Benin': 12123200, 'Burundi': 11890784,
                      'Tunisia': 11818619, 'Bolivia': 11673021, 'Belgium': 11589623, 'Haiti': 11402528,
                      'Cuba': 11326616, 'South Sudan': 11193725, 'Dominican Republic': 10847910, 'Greece': 10423054,
                      'Jordan': 10203134, 'Portugal': 10196709, 'Azerbaijan': 10139177, 'Sweden': 10099265,
                      'Honduras': 9904607, 'United Arab Emirates': 9890402, 'Hungary': 9660351, 'Tajikistan': 9537645,
                      'Belarus': 9449323, 'Austria': 9006398, 'Papua New Guinea': 8947024, 'Serbia': 8737371,
                      'Israel': 8655535, 'Switzerland': 8654622, 'Togo': 8278724, 'Sierra Leone': 7976983,
                      'Laos': 7275560, 'Paraguay': 7132538, 'Bulgaria': 6948445, 'Libya': 6871292, 'Lebanon': 6825445,
                      'Nicaragua': 6624554, 'Kyrgyzstan': 6524195, 'El Salvador': 6486205, 'Singapore': 5850342,
                      'Denmark': 5792202, 'Finland': 5540720, 'Slovakia': 5459642, 'Norway': 5421241, 'Oman': 5106626,
                      'Costa Rica': 5094118, 'Liberia': 5057681, 'Ireland': 4937786,
                      'Central African Republic': 4829767, 'New Zealand': 4822233, 'Mauritania': 4649658,
                      'Panama': 4314767, 'Kuwait': 4270571, 'Croatia': 4105267, 'Moldova': 4033963, 'Georgia': 3989167,
                      'Eritrea': 3546421, 'Uruguay': 3473730, 'Bosnia and Herzegovina': 3280819, 'Mongolia': 3278290,
                      'Armenia': 2963243, 'Jamaica': 2961167, 'Qatar': 2881053, 'Albania': 2877797,
                      'Lithuania': 2722289, 'Namibia': 2540905, 'Gambia': 2416668, 'Botswana': 2351627,
                      'Gabon': 2225734, 'Lesotho': 2142249, 'Slovenia': 2078938, 'Guinea-Bissau': 1968001,
                      'Latvia': 1886198, 'Bahrain': 1701575, 'Equatorial Guinea': 1402985,
                      'Trinidad and Tobago': 1399488, 'Estonia': 1326535, 'Mauritius': 1271768, 'Cyprus': 1207359,
                      'Djibouti': 988000, 'Fiji': 896445, 'Comoros': 869601, 'Guyana': 786552, 'Bhutan': 771608,
                      'Solomon Islands': 686884, 'Montenegro': 628066, 'Suriname': 586632, 'Maldives': 540544,
                      'Malta': 441543, 'Brunei': 437479, 'Belize': 397628, 'Bahamas': 393244, 'Iceland': 341243,
                      'Vanuatu': 307145, 'Barbados': 287375, 'Samoa': 198414, 'Saint Lucia': 183627, 'Kiribati': 119449,
                      'Seychelles': 98347, 'Antigua and Barbuda': 97929, 'Andorra': 77265, 'Dominica': 71986,
                      'Marshall Islands': 59190, 'Monaco': 39242, 'Liechtenstein': 38128, 'San Marino': 33931,
                      'Palau': 18094}

country_population = {
    "China": 1439323776,
    "India": 1380004385,
    "United States": 331002651,
    "Indonesia": 273523615,
    "Pakistan": 220892340,
    "Brazil": 212559417,
    "Nigeria": 206139589,
    "Bangladesh": 164689383,
    "Russia": 145934462,
    "Mexico": 128932753,
    "Japan": 126476461,
    "Ethiopia": 114963588,
    "Philippines": 109581078,
    "Egypt": 102334404,
    "Vietnam": 97338579,
    "DR Congo": 89561403,
    "Turkey": 84339067,
    "Iran": 83992949,
    "Germany": 83783942,
    "Thailand": 69799978,
    "United Kingdom": 67886011,
    "France": 65273511,
    "Italy": 60461826,
    "Tanzania": 59734218,
    "South Africa": 59308690,
    "Myanmar": 54409800,
    "Kenya": 53771296,
    "South Korea": 51269185,
    "Colombia": 50882891,
    "Spain": 46754778,
    "Uganda": 45741007,
    "Argentina": 45195774,
    "Algeria": 43851044,
    "Sudan": 43849260,
    "Ukraine": 43733762,
    "Iraq": 40222493,
    "Afghanistan": 38928346,
    "Poland": 37846611,
    "Canada": 37742154,
    "Morocco": 36910560,
    "Saudi Arabia": 34813871,
    "Uzbekistan": 33469203,
    "Peru": 32971854,
    "Angola": 32866272,
    "Malaysia": 32365999,
    "Mozambique": 31255435,
    "Ghana": 31072940,
    "Yemen": 29825964,
    "Nepal": 29136808,
    "Venezuela": 28435940,
    "Madagascar": 27691018,
    "Cameroon": 26545863,
    "C_te d'Ivoire": 26378274,
    "North Korea": 25778816,
    "Australia": 25499884,
    "Niger": 24206644,
    "Taiwan": 23816775,
    "Sri Lanka": 21413249,
    "Burkina Faso": 20903273,
    "Mali": 20250833,
    "Romania": 19237691,
    "Malawi": 19129952,
    "Chile": 19116201,
    "Kazakhstan": 18776707,
    "Zambia": 18383955,
    "Guatemala": 17915568,
    "Ecuador": 17643054,
    "Syria": 17500658,
    "Netherlands": 17134872,
    "Senegal": 16743927,
    "Cambodia": 16718965,
    "Chad": 16425864,
    "Somalia": 15893222,
    "Zimbabwe": 14862924,
    "Guinea": 13132795,
    "Rwanda": 12952218,
    "Benin": 12123200,
    "Burundi": 11890784,
    "Tunisia": 11818619,
    "Bolivia": 11673021,
    "Belgium": 11589623,
    "Haiti": 11402528,
    "Cuba": 11326616,
    "South Sudan": 11193725,
    "Dominican Republic": 10847910,
    "Czech Republic (Czechia)": 10708981,
    "Greece": 10423054,
    "Jordan": 10203134,
    "Portugal": 10196709,
    "Azerbaijan": 10139177,
    "Sweden": 10099265,
    "Honduras": 9904607,
    "United Arab Emirates": 9890402,
    "Hungary": 9660351,
    "Tajikistan": 9537645,
    "Belarus": 9449323,
    "Austria": 9006398,
    "Papua New Guinea": 8947024,
    "Serbia": 8737371,
    "Israel": 8655535,
    "Switzerland": 8654622,
    "Togo": 8278724,
    "Sierra Leone": 7976983,
    "Hong Kong": 7496981,
    "Laos": 7275560,
    "Paraguay": 7132538,
    "Bulgaria": 6948445,
    "Libya": 6871292,
    "Lebanon": 6825445,
    "Nicaragua": 6624554,
    "Kyrgyzstan": 6524195,
    "El Salvador": 6486205,
    "Turkmenistan": 6031200,
    "Singapore": 5850342,
    "Denmark": 5792202,
    "Finland": 5540720,
    "Congo": 5518087,
    "Slovakia": 5459642,
    "Norway": 5421241,
    "Oman": 5106626,
    "State of Palestine": 5101414,
    "Costa Rica": 5094118,
    "Liberia": 5057681,
    "Ireland": 4937786,
    "Central African Republic": 4829767,
    "New Zealand": 4822233,
    "Mauritania": 4649658,
    "Panama": 4314767,
    "Kuwait": 4270571,
    "Croatia": 4105267,
    "Moldova": 4033963,
    "Georgia": 3989167,
    "Eritrea": 3546421,
    "Uruguay": 3473730,
    "Bosnia and Herzegovina": 3280819,
    "Mongolia": 3278290,
    "Armenia": 2963243,
    "Jamaica": 2961167,
    "Qatar": 2881053,
    "Albania": 2877797,
    "Puerto Rico": 2860853,
    "Lithuania": 2722289,
    "Namibia": 2540905,
    "Gambia": 2416668,
    "Botswana": 2351627,
    "Gabon": 2225734,
    "Lesotho": 2142249,
    "North Macedonia": 2083374,
    "Slovenia": 2078938,
    "Guinea-Bissau": 1968001,
    "Latvia": 1886198,
    "Bahrain": 1701575,
    "Equatorial Guinea": 1402985,
    "Trinidad and Tobago": 1399488,
    "Estonia": 1326535,
    "Timor-Leste": 1318445,
    "Mauritius": 1271768,
    "Cyprus": 1207359,
    "Eswatini": 1160164,
    "Djibouti": 988000,
    "Fiji": 896445,
    "R¨¦union": 895312,
    "Comoros": 869601,
    "Guyana": 786552,
    "Bhutan": 771608,
    "Solomon Islands": 686884,
    "Macao": 649335,
    "Montenegro": 628066,
    "Luxembourg": 625978,
    "Western Sahara": 597339,
    "Suriname": 586632,
    "Cabo Verde": 555987,
    "Micronesia": 548914,
    "Maldives": 540544,
    "Malta": 441543,
    "Brunei": 437479,
    "Guadeloupe": 400124,
    "Belize": 397628,
    "Bahamas": 393244,
    "Martinique": 375265,
    "Iceland": 341243,
    "Vanuatu": 307145,
    "French Guiana": 298682,
    "Barbados": 287375,
    "New Caledonia": 285498,
    "French Polynesia": 280908,
    "Mayotte": 272815,
    "Sao Tome & Principe": 219159,
    "Samoa": 198414,
    "Saint Lucia": 183627,
    "Channel Islands": 173863,
    "Guam": 168775,
    "Cura_ao": 164093,
    "Kiribati": 119449,
    "Grenada": 112523,
    "St. Vincent & Grenadines": 110940,
    "Aruba": 106766,
    "Tonga": 105695,
    "U.S. Virgin Islands": 104425,
    "Seychelles": 98347,
    "Antigua and Barbuda": 97929,
    "Isle of Man": 85033,
    "Andorra": 77265,
    "Dominica": 71986,
    "Cayman Islands": 65722,
    "Bermuda": 62278,
    "Marshall Islands": 59190,
    "Northern Mariana Islands": 57559,
    "Greenland": 56770,
    "American Samoa": 55191,
    "Saint Kitts & Nevis": 53199,
    "Faeroe Islands": 48863,
    "Sint Maarten": 42876,
    "Monaco": 39242,
    "Turks and Caicos": 38717,
    "Saint Martin": 38666,
    "Liechtenstein": 38128,
    "San Marino": 33931,
    "Gibraltar": 33691,
    "British Virgin Islands": 30231,
    "Caribbean Netherlands": 26223,
    "Palau": 18094,
    "Cook Islands": 17564,
    "Anguilla": 15003,
    "Tuvalu": 11792,
    "Wallis & Futuna": 11239,
    "Nauru": 10824,
    "Saint Barthelemy": 9877,
    "Saint Helena": 6077,
    "Saint Pierre & Miquelon": 5794,
    "Montserrat": 4992,
    "Falkland Islands": 3480,
    "Niue": 1626,
    "Tokelau": 1357,
    "Holy See": 801
}
