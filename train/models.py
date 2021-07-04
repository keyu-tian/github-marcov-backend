from django.db import models


class Station(models.Model):
    name_cn = models.CharField(max_length=512, null=False)
    jingdu = models.FloatField(blank=True)
    weidu = models.FloatField(blank=True)
    city = models.ForeignKey('country.City', on_delete=models.SET_NULL, null=True, blank=True)


class Trian(models.Model):
    name = models.CharField(max_length=64, null=False)
    dept_date = models.CharField(max_length=64, null=True, blank=True)
    dept_time = models.CharField(max_length=64, null=True, blank=True)
    dept_city = models.ForeignKey('country.City', related_name='start_train', on_delete=models.SET_NULL, null=True, blank=True)
    dept_station = models.ForeignKey('train.Station', related_name='start_train', on_delete=models.SET_NULL, null=True, blank=True)
    arri_date = models.CharField(max_length=64, null=True, blank=True)
    arri_time = models.CharField(max_length=64, null=True, blank=True)
    arri_city = models.ForeignKey('country.City', related_name='end_train', on_delete=models.SET_NULL, null=True, blank=True)
    arri_station = models.ForeignKey('train.Station', related_name='end_train', on_delete=models.SET_NULL, null=True, blank=True)
    interval = models.CharField(max_length=128, blank=True)
    kilometer = models.IntegerField(blank=True, null=True)
    type = models.CharField(max_length=128, blank=True)
    schedule_station = models.ManyToManyField(Station, through='train.MidStation')


class MidStation(models.Model):
    index = models.IntegerField()
    arri_date = models.IntegerField()  # 出发当天为0，出发后一天为1
    arri_time = models.TimeField()
    station = models.ForeignKey(Station, related_name='pass_by_train', on_delete=models.CASCADE)
    train = models.ForeignKey(Trian, related_name='mid_station', on_delete=models.CASCADE)
