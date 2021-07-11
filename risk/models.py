from django.db import models


# Create your models here.
class RiskArea(models.Model):
    level = models.IntegerField(verbose_name='风险等级', default=0, null=False)  # 分为两种：高和中
    province = models.CharField(verbose_name='省份名', max_length=255)
    city = models.CharField(verbose_name='城市名', max_length=255)
    address = models.CharField(verbose_name='具体地址', max_length=255, default='未知')
    jingdu = models.FloatField(blank=True, null=True)
    weidu = models.FloatField(blank=True, null=True)
