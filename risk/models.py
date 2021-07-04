from django.db import models
from utils.cast import encode, decode


# Create your models here.
class RiskArea(models.Model):

    level = models.IntegerField(verbose_name='风险等级', default=0, null=False)  # 分为两种：高和中
    province = models.CharField(verbose_name='省份名', max_length=255)
    city = models.ForeignKey('country.City', related_name='owned_risk_area', on_delete=models.SET_NULL, null=True)
    address = models.CharField(verbose_name='具体地址', max_length=255, default='未知')
