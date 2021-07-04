from django.db import models
from utils.cast import encode, decode


# Create your models here.
class Flight(models.Model):

    code = models.CharField(verbose_name='班次号', max_length=255, unique=True)
    dept_time = models.CharField(verbose_name='出发时间', max_length=255, default='')
    dept_city = models.ForeignKey('country.City', related_name='start_flight', on_delete=models.SET_NULL, null=True, blank=True)
    arri_time = models.CharField(verbose_name='到达时间', max_length=255, default='')
    arri_city = models.ForeignKey('country.City', related_name='end_flight', on_delete=models.SET_NULL, null=True, blank=True)
    condition = models.CharField(verbose_name='航班状态', max_length=255, default='')


class Airport(models.Model):

    name = models.CharField(verbose_name='机场名字', max_length=255)
    city = models.ForeignKey('country.City', related_name='owned_airport', on_delete=models.SET_NULL, null=True, blank=True)
    jingdu = models.FloatField(blank=True, null=True)
    weidu = models.FloatField(blank=True, null=True)