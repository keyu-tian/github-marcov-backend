import json
import random

import requests

epidemic_id = '1107712'
joke_id = '1107713'
chat_id = '1107714'
chat_service_id = 'S55266'
epid_service_id = 'S55267'
api_key = '8dAUBvIXXvpg9DBrMSEXcDvu'
sec_key = 'fkfGbvMEDCSPVhVBn7OgWprfbkFGdjOi'
access_token = '24.f021f72ef0d5319c65974dc23ea84c36.2592000.1628783775.282335-24541350'


def get_access_token():
    url = f'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={api_key}&client_secret={sec_key}&'
    access_token = json.loads(requests.post(url=url).content)['access_token']
    print(f'access_token: {access_token}')
    return access_token


def chat_query(user_inp, session_id):
    post_data = {
        'log_id': 15712,
        'request': {
            'query': user_inp,
            'user_id': f'marcov19-xya',  # 到时候弄成用户ID
            'query_info': {
                'type': 'TEXT',
                'source': 'ASR',  # ASR, KEYBOARD
                'asr_candidates': [],
            },
        },
        'version': '2.0',
        'service_id': chat_service_id,
        'session_id': session_id,
        'dialog_state': {
            'contexts': {
                'SYS_REMEMBERED_SKILLS': [
                    "",
                ],
            }
        }
    }
    
    res = json.loads(
        requests.post(
            url=f'https://aip.baidubce.com/rpc/2.0/unit/service/chat?access_token={access_token}',
            json=post_data
        ).content
    )
    if res['error_code'] != 0:
        return '', f"[err {res['error_code']}] [{res['error_msg']}]"
    say = res['result']['response_list'][0]['action_list'][0]['say']
    
    for x in {
        '我会再学习更多疫情知识',
        '不知道应该怎么答复',
    }:
        if x in say:
            return '', say
        
    say.replace('小度', random.choice(['小嘤', '我', '俺', '本AI']))
    
    return res['result']['session_id'], say


# if __name__ == '__main__':
#     while True:
#         chat_input = input('请说话>>>>')
#         result_say = unit_chat(chat_input)
#         print("unit输出", result_say)
#         if chat_input == 'Q' or chat_input == 'q':
#             break
