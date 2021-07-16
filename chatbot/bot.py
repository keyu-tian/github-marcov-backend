import random

from chatbot.chat_util import join_rand_punc, rand_beg_word, rand_end_punc, rand_end_face

info = '美国疫情blabla结束'
info = join_rand_punc([
    rand_beg_word(),
    random.choice([
        '情况是这样的',
        '情况是这样子',
        '我来回答您',
        '让我看一下',
        '让我看一下',
        'emm.. 我看看',
        'emm.. 哦，是这样子的',
        '这题我会',
        '我我我来回答您',
    ]),
    info,
])
info += rand_end_punc() + rand_end_face()


print(info)

