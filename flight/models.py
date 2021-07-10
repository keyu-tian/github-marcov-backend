from django.db import models
from country.models import City


class Airport(models.Model):
    name = models.CharField(verbose_name='机场名', max_length=255)
    airport_code = models.CharField(verbose_name='机场代码', max_length=255)
    city = models.ForeignKey(to=City, on_delete=models.SET_NULL, related_name='city_airport_set', blank=True, null=True)


class Flight(models.Model):
    code = models.CharField(primary_key=True, unique=True, max_length=64, db_index=True, null=False)
    dept_time = models.CharField(verbose_name='出发时间', max_length=255, default='')
    dept_airport = models.ForeignKey(to=Airport, related_name='start_flight', on_delete=models.SET_NULL, null=True, blank=True)
    arri_time = models.CharField(verbose_name='到达时间', max_length=255, default='')
    arri_airport = models.ForeignKey(to=Airport, related_name='end_flight', on_delete=models.SET_NULL, null=True, blank=True)
    condition = models.CharField(verbose_name='航班状态', max_length=255, default='')
