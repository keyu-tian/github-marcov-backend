from django.db import models

DT_LENGTH = 80


class Station(models.Model):
    name_ch = models.CharField(primary_key=True, unique=True, max_length=DT_LENGTH, db_index=True, null=False)
    jingdu = models.FloatField(blank=True, null=True)
    weidu = models.FloatField(blank=True, null=True)
    city = models.ForeignKey('country.City', on_delete=models.SET_NULL, null=True, blank=True)


class Train(models.Model):
    name = models.CharField(primary_key=True, unique=True, max_length=DT_LENGTH, db_index=True, null=False)  # 火车号
    dept_date = models.CharField(max_length=DT_LENGTH, null=True, blank=True)
    dept_time = models.CharField(max_length=DT_LENGTH, null=True, blank=True)
    dept_city = models.ForeignKey('country.City', related_name='start_train', on_delete=models.SET_NULL, null=True, blank=True)
    dept_station = models.ForeignKey('train.Station', related_name='start_train', on_delete=models.SET_NULL, null=True, blank=True)
    arri_date = models.CharField(max_length=DT_LENGTH, null=True, blank=True)
    arri_time = models.CharField(max_length=DT_LENGTH, null=True, blank=True)
    arri_city = models.ForeignKey('country.City', related_name='end_train', on_delete=models.SET_NULL, null=True, blank=True)
    arri_station = models.ForeignKey('train.Station', related_name='end_train', on_delete=models.SET_NULL, null=True, blank=True)
    interval = models.CharField(max_length=DT_LENGTH, blank=True)
    kilometer = models.CharField(max_length=256, blank=True, null=True)
    type = models.CharField(max_length=128, blank=True)
    schedule_station = models.ManyToManyField(Station, through='train.MidStation')


class MidStation(models.Model):
    index = models.IntegerField()
    arri_date = models.CharField(max_length=DT_LENGTH, blank=True)
    arri_time = models.CharField(max_length=DT_LENGTH, blank=True)
    station = models.ForeignKey(Station, related_name='pass_by_train', on_delete=models.CASCADE)
    train = models.ForeignKey(Train, related_name='mid_station', on_delete=models.CASCADE)

    class Meta:
        ordering = ('index',)
