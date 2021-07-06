from django.db import models


# Create your models here.
class HistoryEpidemicData(models.Model):
    date = models.CharField(verbose_name='日期', max_length=255)
    country_ch = models.CharField(max_length=512, blank=True)
    province_ch = models.CharField(max_length=512, blank=True)
    city_ch = models.CharField(max_length=512, blank=True)
    province_total_died = models.IntegerField(blank=True, null=True)
    province_total_cured = models.IntegerField(blank=True, null=True)
    province_total_confirmed = models.IntegerField(blank=True, null=True)
    province_new_died = models.IntegerField(blank=True, null=True)
    province_new_cured = models.IntegerField(blank=True, null=True)
    province_new_confirmed = models.IntegerField(blank=True, null=True)
    city_total_died = models.IntegerField(blank=True, null=True)
    city_total_cured = models.IntegerField(blank=True, null=True)
    city_total_confirmed = models.IntegerField(blank=True, null=True)
    city_new_died = models.IntegerField(blank=True, null=True)
    city_new_cured = models.IntegerField(blank=True, null=True)
    city_new_confirmed = models.IntegerField(blank=True, null=True)
