import json
import random
import string
import hashlib

from datetime import datetime

from django.template.loader import render_to_string
from django.views import View
from django.db.utils import IntegrityError, DataError

from analysis.views import country_analyse_data_res
from epidemic.models import HistoryEpidemicData
from epidemic.views import map_today_city_data_res
from marcov19.settings import SERVER_HOST
from meta_config import SPIDER_DATA_DIRNAME
from user.models import User, VerifyCode, Follow
from user.hypers import *
from utils.cast import cur_time
from utils.country_dict import country_dict
from utils.dict_ch import province_dict_ch, district_dict
from utils.email_sender import send_code, send_follow
from utils.meta_wrapper import JSR


def hash_password(pwd):
    m = hashlib.md5()
    m.update(pwd.encode('utf-8'))
    m.update(b"It's MarCov!")
    return m.digest()


class Register(View):
    @JSR('status')
    def post(self, request):
        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != {'account', 'name', 'pwd', 'ver'}:
            return 1,
        if not CHECK_ACC(kwargs['account']):
            return 3,
        if not CHECK_PWD(kwargs['pwd']):
            return 5,
        if not CHECK_NAME(kwargs['name']):
            return 4,
        kwargs.update({'pwd': hash_password(kwargs['pwd'])})
        kwargs.update({'avatar': 'http://' + SERVER_HOST + '/upload/avatar/default.jpg'})
        vc = VerifyCode.objects.filter(code=kwargs['ver'], account=kwargs['account'])
        if not vc.exists():
            return 102,
        vc = vc.get()
        kwargs.pop('ver')

        if datetime.now() < vc.expire_time:
            try:
                u = User.objects.create(**kwargs)
            except IntegrityError:
                return 101,  # 字段unique未满足
            except DataError:
                return -1,  # 诸如某个CharField超过了max_len的错误
            except:
                return -1,
            request.session['is_login'] = True
            request.session['identity'] = u.identity
            request.session['uid'] = u.id
            request.session['name'] = u.name
            request.session.save()
            return 0,
        else:
            return 102,


class SendVer(View):
    @JSR('status')
    def post(self, request):
        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != {'account'}:
            return 1,
        if not CHECK_ACC(kwargs['account']):
            return 3,
        if User.objects.filter(account=kwargs['account']).exists():
            return 101,
        if send_code(kwargs['account'], 'register'):
            return 0,
        else:
            return -1,


class Login(View):
    @JSR('status')
    def post(self, request):
        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != {'account', 'pwd'}:
            return 1
        u = User.objects.filter(account=kwargs['account'])
        if not u.exists():
            return 7
        u = u.get()
        if u.pwd != str(hash_password(kwargs['pwd'])):
            return 5
        request.session['is_login'] = True
        request.session['identity'] = u.identity
        request.session['uid'] = u.id
        request.session['name'] = u.name
        request.session.save()
        try:
            u.save()
        except:
            return -1
        return 0


class Logout(View):
    @JSR('status')
    def post(self, request):
        if request.session.get('is_login', None):
            request.session['is_login'] = False
            request.session.flush()
            return 0
        else:
            request.session.flush()
            return 0


class ForgetPwdSend(View):
    @JSR('status')
    def post(self, request):
        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != {'account'}:
            return 1
        if not CHECK_ACC(kwargs['account']):
            return 3,
        if not User.objects.filter(account=kwargs['account']).exists():
            return 101,
        if send_code(kwargs['account'], 'forget'):
            return 0,
        else:
            return -1,


class ForgetPwdChange(View):
    @JSR('status')
    def post(self, request):
        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != {'account', 'pwd', 'ver'}:
            return 1,
        u = User.objects.filter(account=kwargs['account'])
        if not u.exists():
            return 101,
        u = u.get()
        if not CHECK_PWD(kwargs['pwd']):
            return 5,
        if not VerifyCode.objects.filter(code=kwargs['ver']).exists():
            return 102,
        u.pwd = hash_password(kwargs['pwd'])
        u.save()
        return 0,


class ChangePwd(View):
    @JSR('status')
    def post(self, request):
        kwargs: dict = json.loads(request.body)
        if not {'old_pwd', 'new_pwd', 'new_pwd_2'}.issubset(kwargs.keys()):
            return 1

        u = User.objects.filter(id=request.session['uid'])
        if not u.exists():
            return -1
        u = u.get()

        if str(hash_password(kwargs['old_pwd'])) != u.pwd:
            return 101
        if not CHECK_PWD(kwargs['new_pwd']):
            return 5
        if not CHECK_PWD(kwargs['new_pwd_2']):
            return 5
        if kwargs['new_pwd'] != kwargs['new_pwd_2']:
            return 103
        u.pwd = hash_password(kwargs['new_pwd'])
        try:
            u.save()
        except:
            return -1
        return 0


class ChangeInfo(View):
    @JSR('status')
    def post(self, request):
        try:
            uid = int(request.session.get('uid', None))
        except:
            return -1
        u = User.objects.filter(id=uid)
        if not u.exists():
            return -1
        u = u.get()

        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != {'name', 'avatar'}:
            return 1,
        if kwargs['name'] is not None and not CHECK_NAME(kwargs['name']):
            return 4,
        u.name = kwargs['name']
        if kwargs['avatar'] is not None and not CHECK_AVATAR(kwargs['avatar']):
            return 102,
        u.avatar = kwargs['avatar']

        try:
            u.save()
        except:
            return -1
        return 0


class UserInfo(View):
    @JSR('status', 'name', 'avatar', 'identity', 'uid')
    def get(self, request):
        if not request.session.get('is_login', None):
            return 0, '', '', 1, '',
        try:
            uid = int(request.session.get('uid', None))
        except:
            return 1, '', '', 1, '',
        u = User.objects.filter(id=uid)
        if not u.exists():
            return -1, '', '', 1, '',
        u = u.get()
        return 0, u.name, u.avatar, u.identity, u.id,


class TimeInfo(View):
    @JSR('status', 'time')
    def get(self, request):
        return 0, cur_time()


class Identity(View):
    @JSR('status', 'type')
    def get(self, request):
        try:
            account = str(request.GET.get('account'))
        except:
            return 1, 0
        u = User.objects.filter(account=account)
        if not u.exists():
            return 0, 0
        u = u.get()
        return 0, u.identity


class UploadPic(View):
    @JSR('status', 'avatar')
    def post(self, request):
        try:
            file = request.FILES.get('file')
        except:
            return 1, ''

        if file.size > MAX_UPLOADED_FSIZE:
            return 102, ''

        if file.name.split('.')[1] not in ['jpg', 'png']:
            return 101, ''

        file_name = ''.join(
            [random.choice(string.ascii_letters + string.digits) for _ in range(FNAME_DEFAULT_LEN)]) + '.' + \
                    str(file.name).split(".")[-1]

        file_path = os.path.join(DEFAULT_AVATAR_ROOT, file_name)
        file_url = 'http://' + SERVER_HOST + '/upload/avatar/' + file_name
        # if not os.path.exists(file_path):
        #     os.makedirs(file_path)
        with open(file_path, 'wb') as dest:
            [dest.write(chunk) for chunk in file.chunks()]
        return 0, file_url


class FollowNew(View):
    @JSR('status')
    def post(self, request):
        try:
            uid = int(request.session.get('uid', None))
            user = User.objects.get(id=uid)
        except:
            return 2,
        kwargs: dict = json.loads(request.body)
        if not {'level', 'mail', 'is_new'}.issubset(kwargs.keys()):
            return 1
        try:
            level = int(kwargs['level'])
            mail = bool(kwargs['mail'])
            is_new = bool(kwargs['is_new'])
        except:
            return 1

        if level == 1:
            if not {'country'}.issubset(kwargs.keys()):
                return 1
            total_data = HistoryEpidemicData.objects.filter(country_ch__icontains=kwargs['country'])
            if total_data.count() == 0:
                return 7
            if is_new:
                fo, flag = Follow.objects.get_or_create(user=user, level=1, country=kwargs['country'])
                if not flag:
                    return 2
            else:
                fo = Follow.objects.filter(user=user, level=1, country=kwargs['country'])
                if not fo.exists():
                    return 3
                fo.delete()
        elif level == 2:
            if not {'province'}.issubset(kwargs.keys()):
                return 1
            total_data = HistoryEpidemicData.objects.filter(province_ch__icontains=kwargs['province'])
            if total_data.count() == 0:
                return 7
            if is_new:
                fo, flag = Follow.objects.get_or_create(user=user, level=2, province=kwargs['province'])
                if not flag:
                    return 2
            else:
                fo = Follow.objects.filter(user=user, level=2, province=kwargs['province'])
                if not fo.exists():
                    return 3
                fo.delete()
        elif level == 3:
            if not {'province', 'city'}.issubset(kwargs.keys()):
                return 1
            if is_new:
                fo, flag = Follow.objects.get_or_create(user=user, level=3, province=kwargs['province'],
                                                        city=kwargs['city'])
                if not flag:
                    return 2
            else:
                fo = Follow.objects.filter(user=user, level=3, province=kwargs['province'], city=kwargs['city'])
                if not fo.exists():
                    return 3
                fo.delete()
        else:
            return 1
        user.is_mail = bool(mail)
        user.save()
        return 0


class FollowData(View):
    @JSR('status', 'data')
    def post(self, request):
        try:
            uid = int(request.session.get('uid', None))
            user = User.objects.get(id=uid)
        except:
            return 2, {}
        follow_set = Follow.objects.filter(user=user)
        return 0, get_follow_data(follow_set)


def get_follow_data(follow_set):
    data = []
    for a in follow_set:
        if a.level == 1:
            population, daily_data = country_analyse_data_res(a.country)
            if daily_data is not None:
                data.append({
                    'country': a.country,
                    'province': '',
                    'city': '',
                    'population': population,
                    'level': 1,
                    'new': daily_data[-1]['new'],
                    'total': daily_data[-1]['total'],
                })
        elif a.level == 2:
            population, daily_data = country_analyse_data_res(a.province)
            if daily_data is not None:
                data.append({
                    'country': '',
                    'province': a.province,
                    'city': '',
                    'population': population,
                    'level': 1,
                    'new': daily_data[-1]['new'],
                    'total': daily_data[-1]['total'],
                })
        else:
            date, city_ret, districts = map_today_city_data_res(a.province, a.city)
            if city_ret is not None:
                data.append({
                    'country': '',
                    'province': a.province,
                    'city': a.city,
                    'population': 0,
                    'level': 1,
                    'new': city_ret['new'],
                    'total': city_ret['total'],
                })
    return data


class FollowSetMail(View):
    @JSR('status')
    def post(self, request):
        try:
            uid = int(request.session.get('uid', None))
            user = User.objects.get(id=uid)
        except:
            return 2,
        kwargs: dict = json.loads(request.body)
        if not {'mail'}.issubset(kwargs.keys()):
            return 1
        try:
            mail = int(kwargs['mail'])
        except:
            return 1
        if mail != 1 and mail != 0:
            return 1

        if user.is_mail is True and mail == 1:
            return 2
        elif user.is_mail is False and mail == 0:
            return 3
        user.is_mail = True if mail == 1 else False
        user.save()
        return user


def send_task_email():
    email_user_list = User.objects.filter(is_mail=True)
    for u in email_user_list:
        tasks = Follow.objects.filter(user=u)
        if tasks:
            # html_message = render_to_string('task/task.html', {'tasks': tasks, 'user': user})
            send_follow(u, get_follow_data(tasks))


class FollowProvince(View):
    @JSR('status', 'data')
    def post(self, request):
        try:
            uid = int(request.session.get('uid', None))
            user = User.objects.get(id=uid)
        except:
            return 2
        res = []
        follow_set = [a.province for a in Follow.objects.filter(user=user, level=2)]
        for a in province_dict_ch.keys():
            res[a] = int(a in follow_set)

        return 0, res


class FollowCountry(View):
    @JSR('status', 'data')
    def post(self, request):
        try:
            uid = int(request.session.get('uid', None))
            user = User.objects.get(id=uid)
        except:
            return 2
        res = []
        follow_set = [a.country for a in Follow.objects.filter(user=user, level=1)]
        for a in country_dict.values():
            res[a] = int(a in follow_set)

        return 0, res


class FollowCity(View):
    @JSR('status', 'data')
    def post(self, request):
        try:
            uid = int(request.session.get('uid', None))
            user = User.objects.get(id=uid)
        except:
            return 2
        try:
            province = json.loads(request.body)['province']
        except:
            return 1
        res = []
        follow_set = [a.city for a in Follow.objects.filter(user=user, level=3, province=province)]
        for a in district_dict[province].keys():
            res[a] = int(a in follow_set)

        return 0, res
