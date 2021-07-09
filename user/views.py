import json
import random
import string
import hashlib

from datetime import datetime

from django.views import View
from django.db.utils import IntegrityError, DataError

from marcov19.settings import SERVER_HOST
from user.models import User, VerifyCode
from user.hypers import *
from utils.cast import cur_time
from utils.email_sender import send_code
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
