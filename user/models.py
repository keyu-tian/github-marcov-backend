from datetime import datetime
from django.db import models
from django.db.models import Q

from meta_config import TIME_FMT
from user.hypers import *


class User(models.Model):
    @property
    def ver_code(self):
        q = VerifyCode.objects.filter(account=self.account)
        if q.exists():
            q.get()
            if q.expire_time > datetime.now():
                return q.code
        return None

    @staticmethod
    def get_all_admin():
        return User.objects.filter(Q(identity=3) | Q(identity=4))

    name = models.CharField(verbose_name='姓名', max_length=32)
    account = models.CharField(verbose_name='邮箱', max_length=64, unique=True)
    pwd = models.CharField(verbose_name='密码', max_length=64)
    identity = models.IntegerField(verbose_name='身份', choices=IDENTITY_CHS, default=1)
    avatar = models.CharField(blank=True, verbose_name="头像路径", max_length=512, default='')
    login_date = models.DateField(blank=True, verbose_name='最近登录时间', auto_now_add=True)
    wrong_count = models.IntegerField(blank=True, verbose_name='最近一天密码错误次数', default=0)


class VerifyCode(models.Model):
    code = models.CharField(max_length=20, verbose_name='验证码')
    account = models.EmailField(max_length=50, verbose_name='用户邮箱', null=True, default='')
    expire_time = models.DateTimeField(null=True, verbose_name='过期时间')
    type = models.IntegerField(choices=VERCODE_CHS, default=1)

    class Meta:
        verbose_name = '验证码'
        verbose_name_plural = verbose_name
