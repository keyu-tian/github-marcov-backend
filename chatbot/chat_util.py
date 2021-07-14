CHAT_DEBUG = True

import re
import random
import datetime
from collections import OrderedDict
from time import time

endswith_ch_punc = lambda s: s[-1] in {'?', '？', '¿', '!', '！', '。', '.', '~'}


def greet_based_on_time():
    h = datetime.datetime.now().hour + datetime.datetime.now().minute / 60
    if 0 <= h <= 5.5:
        return random.choice([
            '夜猫子，晚上好！',
            '还在肝呢？晚上好！',
            '别肝了，晚上好！',
            '哥，DDL赶完了吗就逛网站！',
            '哥，别肝了！',
        ])
    if h <= 11.5:
        return random.choice(['早上好', '早安']) + random.choice(['~ ', '，']) + random.choice([
            '早起的鸟儿有虫吃！',
            '一日之计在于晨！',
            '你是通了还是起了属于是？' if CHAT_DEBUG else '吃了吗？',
            '爬了吗？哦不是，起床了吗？' if CHAT_DEBUG else '早饭吃了吗？',
        ]) + random.choice(['🌞', '🌤', '😎', '🙂'])
    if h <= 18:
        return random.choice(['下午好', '下午好呀']) + random.choice(['~ ', '，', '。']) + random.choice([
            '午饭吃饱了吗？',
            '不是吧、不是吧？不会有人才起床吧？吃饭了吗' if CHAT_DEBUG else '吃了吗',
            '该不会才起床吧？吃饭了吗' if CHAT_DEBUG else '吃了没',
            '宝，才起来？我给你热了早饭，记得吃哦' if CHAT_DEBUG else '午饭吃了吗',
        ]) + random.choice(['🍚？', '🍱？', '🍱？', '🥘？'])
    return random.choice(['晚上好', '晚上好呀']) + random.choice(['~ ', '，']) + random.choice([
        '晚餐吃的如何？',
        '该不会才睡醒午觉吧？吃饭了吗' if CHAT_DEBUG else '吃了吗',
        '据说晚上是年轻人精力最旺盛的时候' if CHAT_DEBUG else '晚饭吃了吗',
    ]) + random.choice(['🌛？', '🌚？', '🌝？'])


def del_stop_words(s: str):
    if s == '？':
        s = '?'
    rs = str(s)
    s = ' '.join(map(str.strip, s.split())).strip('，').strip('。')
    s = ''.join(ch for ch in s if ch not in {
        '啊', '哦', '呢', '嗯', '恩', '咦', '呗', '唉', '哎', '呵', '呀', '哇', '呃', '咚', '之', '哉', '吧', '哒',
        '；', ';', '“', '”', '"', '\'',
        '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '+', '=', '\\', '/', '|', '`', '~',
    })
    s = ' '.join(map(str.strip, s.split())).replace('，，', '，').replace('，。', '。').strip('。')
    s = re.sub(
        '请问|问一下|我想问|云云|于是乎|由此可见|以便|大概|大体|大抵|'
        '有望|可能|即是|似乎|好似|好像|好象|似的|将会|即将|比方|比如|例如|像是|'
        '若是|若要|如果是|如果说|如果|倘或|倘然|倘若|倘使|然而|的话|也就是说|就是说',
        '', s
    )
    s = ' '.join(map(str.strip, s.split())).replace('，，', '，').replace('，。', '。').strip('。')
    
    if '不知道' in s:
        s = s.replace('不知道', random.choice(['不知道', '不知道', '不明白']))
    if '你是谁' in s:
        s = s.replace('你是谁', random.choice(['你是谁', '你是谁', '你是谁', '你是谁', '你是何方神圣', '你是上帝', '你是什么']))
    if '我是谁' in s:
        s = s.replace('我是谁', random.choice(['我是谁', '我是谁你知道吗', '你打听打听我的名字', '你知道我的名字吗', '我是你']))

    res = []
    for ch in s:
        if ch == '我':
            ch = random.choice(['我', '我', '我', '俺'])
        if ch == '你':
            ch = random.choice(['你', '你', '您'])
        res.append(ch)
    s = ''.join(res)
    
    if len(s) == 0:
        s = rs
    
    return s


_rich_beg_word = OrderedDict(dict(
    您好=7.5, 亲=1.5, 亲亲=0.75,
    友友=0.75, 宝=0.6, 乖宝=0.4, 我的宝=0.25,
))
_rich_sep_punc = OrderedDict({
    '，': 10, ' ': 1, '~': 2,
    '~~': 0.5,
})
_rich_end_word = OrderedDict({
    '': 8, '哦': 1, '啊': 1, '哈': 1, '呀': 1,
    '嘤': 0.9, '嘿': 0.1, '嗷': 0.2, '惹': 0.1, '吼': 0.1, '害': 0.1,
})
_rich_end_punc = OrderedDict({
    '。': 10, '！': 2, '..': 1,
    '（': 0.5, '（x': 0.25, '（x）': 0.2, '（）': 0.2, 'hh': 0.25,
})
_rich_end_query = OrderedDict({
    '？': 6,
    '（？': 0.25, '（？）': 0.2, '¿': 0.2, '（¿': 0.1, '（¿）': 0.1,
})
_rich_end_face = OrderedDict({
    '🙂': 3, '~': 1, '~~': 0.5,
    '😊': 2, '😝': 2, '😉': 2, '😃': 1, '😏': 1, '🤗': 1,
    '🌞': 1, '😀': 1, '😎': 1, '😶': 1,
    '🐵': 0.5, '🤪': 0.5, '😅': 0.75, '🙃': 0.25,
    '(x': 0.9, '（x': 0.9,
    '(x)': 0.9, '（x）': 0.9,
    '(X': 0.9, '（X': 0.9,
})


# 必定疑问
_rich_no_idea_sent = OrderedDict({
    '抱歉，我不太明白，您能再说一次吗': 1,
    '抱歉，我没有搞懂您的意思，您能再说一次吗': 1,
    '抱歉，我有点糊涂了': 1,
    '竟无语凝噎': 1,
    '我听不懂，你在用两个脑子思考？': 0.75,
    '我听不懂，你在用两个脑子思考？🐒': 0.75,
    '喵喵喵': 0.5,
    '喵喵喵？': 0.5,
    '你好会说呀': 0.5,
    '你好会说呀😅': 0.75,
    '蜜雪冰城甜蜜蜜': 0.8,
    '你爱我，我爱你，蜜雪冰城甜蜜蜜': 0.8,
    '原来我被你整无语了': 0.5, '🐒来我被你整🈚🌧了': 0.5,
    '我都被你整无语了': 0.1, '我都被你整🈚🌧了': 0.2,
})
# 必定陈述
_rich_tricky_sent = OrderedDict({
    '抱歉，我不太明白该怎么回答这个问题': 1,
    '抱歉，我不知道该怎么回答这个问题': 1,
    '抱歉，我无法回答': 1,
    '我听不懂，但我大为震撼': 1.5,
    '我看不懂，但我大为震撼': 0.5,
    '您敢问，小的不敢答': 0.75,
    '我不知道该说什么（危': 0.75,
    '我不知道该说什么（逃': 0.5,
    '这个口味的冰红茶🧃挺好喝的': 0.95,
    '这个口味的冰红茶🧃还挺好喝的': 0.95,
    '这个风味的冰红茶🧃挺好喝的': 0.95,
    '这个风味的冰红茶🧃还挺好喝的': 0.95,
    '诶这个口味的冰红茶🧃挺好喝的': 0.95,
    '诶这个口味的冰红茶🧃还挺好喝的': 0.95,
    '诶这个风味的冰红茶🧃挺好喝的': 0.95,
    '诶这个风味的冰红茶🧃还挺好喝的': 0.95,
    '我听不懂，你在用两个脑子思考': 0.75,
})
# 大部分陈述
_rich_juan_sent = OrderedDict({
    '别卷了，快来和我一起摸🐟吧': 2,
    '别卷了，快来和我一起摸🐠吧': 2,
    '别卷了，快来和我一起摸鱼吧': 1,
    '别卷了，别卷了': 1,
    '活到老，卷到老': 1,
    '卷卷相报何时了': 1,
    '你就是卷王？': 1,
    '开卷有益': 1,
    '卷 翻 天': 1,
    '卷卷有爷名': 1,
    '三椽函宇宙，一卷肇乾坤': 1,
})
# 大部分陈述
_rich_dev_sent = OrderedDict({
    '您搁着 de de-bug 呢？': 1,
    '您搁着写 bug 呢？': 1,
    '你 用 户 故 事 格 式 写 错 了': 1,
    '你测试用例格式写错了': 1,
    'git push --force，我可会了': 1,
    'git push --force，嘻嘻嘻~': 1,
    'git push --force，嘿嘿嘿~': 1,
    '代码审查过了吗': 1,
    '你站会不会迟到了吧': 1,
    '刚签到了，你去上厕所了？': 1,
    '你 情 绪 图 没 填': 1,
    '你 情 绪 图 没 填 啊': 1,
    '摸🐟子不🐟鱼': 1,
})
# 大部分疑问
_rich_greet = OrderedDict({
    '我是小嘤🌸，可解答疫情情况、新闻、政策等问题，请问有什么问题吗': 1,
    '我是小嘤🌸，可解答疫情情况、新闻、政策等问题，您有什么疑惑吗': 1,
    '我是小嘤🌸，可解答疫情情况、新闻、政策等问题，您有任何问题都可以问我': 1,
    '我是小嘤🌸，可解答疫情情况、新闻、政策等问题，很乐意为您答疑解惑！': 1,
    '我是小嘤🌸，可解答疫情情况、新闻、政策等问题，有什么我可以帮您': 1,
    '我是小嘤🌸，可解答疫情情况、新闻、政策等问题，有什么我可以解惑的吗': 1,
    '我是小嘤🌸，可解答疫情情况、新闻、政策等问题，有什么问题问我就好。': 1,
    '我是小嘤🌸，可解答疫情情况、新闻、政策等问题，您可以问我疫情问题，或者和我聊天哦。': 1,
    '我是小嘤🌸，可解答疫情情况、新闻、政策等问题，问我疫情相关问题或者聊天都可以的哦~': 1,
    '我是小嘤🌸，可解答疫情情况、新闻、政策等问题，您有任何问题，都可以问我这个小机灵鬼哦~': 1,
    '我是小嘤🌸，可解答疫情情况、新闻、政策等问题，您有任何问题，都可以问我这个小机灵鬼儿哦~': 1,
    '我是小嘤🌸，可解答疫情情况、新闻、政策等问题，等您消息等好久了，快来问我吧~': 2,
    '我是小嘤🌸，可解答疫情情况、新闻、政策等问题，等亲消息等到荷花都要谢了，有什么问题快来问我吧~': 2,
})

dict_dict = {k: globals()[k] for k in dir() if k.startswith('_rich_')}
# [print(k + '  ', globals()[k]) for k in dir() if k.startswith('rich_')]

# print('\n__clean_up = lambda od: OrderedDict({k: v for k, v in od.items() if v >= 0.99})')
# for k, v in dict_dict.items():
#     print(f'{k.replace("rich", "simple")} = __clean_up({k})')
# print('')
# for k, v in dict_dict.items():
#     print(f'rand{k} = lambda: random.choices(list({k}.keys()), weights=list({k}.values()), k=1)[0]')
#     k = k.replace('rich', 'simple')
#     print(f'rand{k} = lambda: random.choices(list({k}.keys()), weights=list({k}.values()), k=1)[0]')
# print('')
# for k, v in dict_dict.items():
#     k = k.replace('_rich_', '')
#     print(f'rand_{k} = rand_rich_{k} if CHAT_DEBUG else rand_simple_{k}')

random.seed(time() * 10)

#########################################################################

__clean_up = lambda od: OrderedDict({k: v for k, v in od.items() if v >= 0.99})
_simple_beg_word = __clean_up(_rich_beg_word)
_simple_dev_sent = __clean_up(_rich_dev_sent)
_simple_end_face = __clean_up(_rich_end_face)
_simple_end_punc = __clean_up(_rich_end_punc)
_simple_end_query = __clean_up(_rich_end_query)
_simple_end_word = __clean_up(_rich_end_word)
_simple_greet = __clean_up(_rich_greet)
_simple_juan_sent = __clean_up(_rich_juan_sent)
_simple_no_idea_sent = __clean_up(_rich_no_idea_sent)
_simple_sep_punc = __clean_up(_rich_sep_punc)
_simple_tricky_sent = __clean_up(_rich_tricky_sent)

rand_rich_beg_word = lambda: random.choices(list(_rich_beg_word.keys()), weights=list(_rich_beg_word.values()), k=1)[0]
rand_simple_beg_word = lambda: random.choices(list(_simple_beg_word.keys()), weights=list(_simple_beg_word.values()), k=1)[0]
rand_rich_dev_sent = lambda: random.choices(list(_rich_dev_sent.keys()), weights=list(_rich_dev_sent.values()), k=1)[0]
rand_simple_dev_sent = lambda: random.choices(list(_simple_dev_sent.keys()), weights=list(_simple_dev_sent.values()), k=1)[0]
rand_rich_end_face = lambda: random.choices(list(_rich_end_face.keys()), weights=list(_rich_end_face.values()), k=1)[0]
rand_simple_end_face = lambda: random.choices(list(_simple_end_face.keys()), weights=list(_simple_end_face.values()), k=1)[0]
rand_rich_end_punc = lambda: random.choices(list(_rich_end_punc.keys()), weights=list(_rich_end_punc.values()), k=1)[0]
rand_simple_end_punc = lambda: random.choices(list(_simple_end_punc.keys()), weights=list(_simple_end_punc.values()), k=1)[0]
rand_rich_end_query = lambda: random.choices(list(_rich_end_query.keys()), weights=list(_rich_end_query.values()), k=1)[0]
rand_simple_end_query = lambda: random.choices(list(_simple_end_query.keys()), weights=list(_simple_end_query.values()), k=1)[0]
rand_rich_end_word = lambda: random.choices(list(_rich_end_word.keys()), weights=list(_rich_end_word.values()), k=1)[0]
rand_simple_end_word = lambda: random.choices(list(_simple_end_word.keys()), weights=list(_simple_end_word.values()), k=1)[0]
rand_rich_greet = lambda: random.choices(list(_rich_greet.keys()), weights=list(_rich_greet.values()), k=1)[0]
rand_simple_greet = lambda: random.choices(list(_simple_greet.keys()), weights=list(_simple_greet.values()), k=1)[0]
rand_rich_juan_sent = lambda: random.choices(list(_rich_juan_sent.keys()), weights=list(_rich_juan_sent.values()), k=1)[0]
rand_simple_juan_sent = lambda: random.choices(list(_simple_juan_sent.keys()), weights=list(_simple_juan_sent.values()), k=1)[0]
rand_rich_no_idea_sent = lambda: random.choices(list(_rich_no_idea_sent.keys()), weights=list(_rich_no_idea_sent.values()), k=1)[0]
rand_simple_no_idea_sent = lambda: random.choices(list(_simple_no_idea_sent.keys()), weights=list(_simple_no_idea_sent.values()), k=1)[0]
rand_rich_sep_punc = lambda: random.choices(list(_rich_sep_punc.keys()), weights=list(_rich_sep_punc.values()), k=1)[0]
rand_simple_sep_punc = lambda: random.choices(list(_simple_sep_punc.keys()), weights=list(_simple_sep_punc.values()), k=1)[0]
rand_rich_tricky_sent = lambda: random.choices(list(_rich_tricky_sent.keys()), weights=list(_rich_tricky_sent.values()), k=1)[0]
rand_simple_tricky_sent = lambda: random.choices(list(_simple_tricky_sent.keys()), weights=list(_simple_tricky_sent.values()), k=1)[0]

rand_beg_word = rand_rich_beg_word if CHAT_DEBUG else rand_simple_beg_word
rand_dev_sent = rand_rich_dev_sent if CHAT_DEBUG else rand_simple_dev_sent
rand_end_face = rand_rich_end_face if CHAT_DEBUG else rand_simple_end_face
rand_end_punc = rand_rich_end_punc if CHAT_DEBUG else rand_simple_end_punc
rand_end_query = rand_rich_end_query if CHAT_DEBUG else rand_simple_end_query
rand_end_word = rand_rich_end_word if CHAT_DEBUG else rand_simple_end_word
rand_greet = rand_rich_greet if CHAT_DEBUG else rand_simple_greet
rand_juan_sent = rand_rich_juan_sent if CHAT_DEBUG else rand_simple_juan_sent
rand_no_idea_sent = rand_rich_no_idea_sent if CHAT_DEBUG else rand_simple_no_idea_sent
rand_sep_punc = rand_rich_sep_punc if CHAT_DEBUG else rand_simple_sep_punc
rand_tricky_sent = rand_rich_tricky_sent if CHAT_DEBUG else rand_simple_tricky_sent

#########################################################################

# rand_test = lambda: rand_beg_word() + rand_sep_punc() + '吃了吗' + rand_end_word() + rand_end_face() + rand_end_punc()
# for _ in range(10):
#     print(rand_test() + '       ' + rand_test())


def join_rand_punc(ls):
    res = [ls[0]]
    for s in ls[1:]:
        res.append(rand_sep_punc())
        res.append(s)
    return ''.join(res)
    

def add_tail(s: str, q: bool):
    if not endswith_ch_punc(s):
        s += rand_end_query() if q else rand_end_punc()
    return s


tricky_keys = {
    '林广艳',
    '林老师',
    '助教',
    'ihome',
    '夏令营',
    '夏零营',
    '夏0营',
    '夏O营',
    '夏o营',
    '保研',
    '谭火彬',
    '贾经冬',
    '宋友',
    '杨晴虹',
    '黄坚',
    '申雪萍',
    '原仓周',
    '原力',
}

juan_keys = {
    '卷了',
    '卷王',
    '开卷',
    '别卷',
    '要卷',
    '还卷',
    '在卷',
    '躺平',
    '互评',
    '权重',
    '卷啊',
    '卷起来',
    '硬卷',
}

dev_keys = {
    'git',
    'bug',
    'Bug',
    'BUG',
    'sudo',
    'rm -r',
    'rm -f',
    '用户故事',
    '测试用例',
    '站会',
    '签到',
    '情绪图',
    '燃尽图',
    '燃烬图',
    '那个女人',
}

