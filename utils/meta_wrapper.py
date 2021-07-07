import functools
import json
import time
from datetime import datetime
from pprint import pformat

from colorama import Fore
from django.http import JsonResponse, HttpResponseForbidden

import meta_config


def JSR(*keys): # 这里的 keys 是 @JSR(...) 里面填的 keys
    
    def decorator(req_func):
        
        @functools.wraps(req_func)
        def wrapper(*args, **kw):
            # args 是被 JSR 装饰的成员函数，所以理论上是有两个参数，第一个是 this 指针（self），第二个是函数唯一的显式参数 request；理论上 kw 是空的
            self, request = args
            req_type = req_func.__name__.upper()
            func_name: str = meta_config.CLS_PARSE_REG.findall(str(type(self)))[0].replace(".views.", ".")
            func_name = '' if len(func_name) < 2 else func_name
            func_name += f'.{req_type}'

            if req_type == 'POST':  # 如果是 POST 请求，输入是从 request.body 来的；这里解析一下 inputs，后面打印用。
                try:
                    inputs = pformat(json.loads(request.body))
                except:
                    inputs = '[cannot preview body]'
            else:   # 如果是 GET 请求，输入是从 request.session 来的；这里解析一下 inputs，后面打印用。
                inputs = f'session: {pformat(dict(request.session))}'
                d_get = dict(request.GET)
                if len(d_get.keys()):
                    inputs += f', GET: {pformat(d_get)}'

            prev_time = time.time() # 这个变量是计算后端实际耗时用的
            try:
                # 【关键】实际就是在这里调用了某个 View 的成员函数
                values = req_func(*args, **kw)
            except Exception as e:
                time_cost = time.time() - prev_time
                time.sleep(0.1)
                # 【关键】这个请求出错了，打印
                print(Fore.MAGENTA + f'[{func_name}] ====! FATAL ERR !==== : {e}, {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
                                     f'\n input: {inputs}, time: {time_cost:.2f}s', flush=True)
                time.sleep(0.1)
                # traceback.print_exc()
                raise e
            else:
                time_cost = time.time() - prev_time
                values = list(values) if isinstance(values, (tuple, list)) else [values]    # 这个是为了判断，如果只有一个返回值，那么就把它转成一个单元素列表
                [values.append('') for _ in range(len(keys) - len(values))]                 # 这个是在给没填的返回值位置自动填充空字符串作为返回值
                ret_dict = dict(zip(keys, values))      # 打包成返回值
                
                if meta_config.DEBUG:
                    c = Fore.RED if ret_dict.get('status', 0) else Fore.GREEN
                    cur_dt = datetime.now()
                    dt_str = cur_dt.strftime("%H:%M:%S.") + f'{float(cur_dt.strftime("0.%f")):.2f}'[-2:]
                    # 【关键】给正常返回的请求打印一下
                    if func_name in ['analysis.CountryAnalyze.POST', 'analysis.DomesticAnalyze.GET', 'analysis.InternationalAnalyze.GET', 'analysis.SearchAnalyse.POST']:
                        ret_str = str(dict(status=ret_dict.get('status', 0)))
                    else:
                        ret_str = pformat(ret_dict)
                    
                    print(c + f'[{func_name}] input: {inputs}\n ret: {ret_str}, time: {time_cost:.2f}s, at [{dt_str}]', flush=True)
                if ret_dict.get('status', 0) == 403:
                    return HttpResponseForbidden()
                
                # 设置 session_id。这个部分不是 tky 写的。
                session_id = request.COOKIES.get('sessionid', None)
                if session_id is None:
                    session_id = request.session.session_key
                ret_dict['sessionid'] = session_id
                response = JsonResponse(ret_dict)
                response.set_cookie(key="sessionid", value=session_id, httponly=False, domain="buaasoft.icu")
                
                return response

        return wrapper

    return decorator
