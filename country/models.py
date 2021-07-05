from django.db import models


class Country(models.Model):
    name_ch = models.CharField(max_length=512, blank=True)
    name_en = models.CharField(max_length=512, blank=True)
    code = models.CharField(max_length=128, blank=True)


class Province(models.Model):
    name_ch = models.CharField(max_length=512, blank=True)
    name_en = models.CharField(max_length=512, blank=True)
    country = models.ForeignKey(to=Country, on_delete=models.CASCADE, related_name='province_set', blank=True, null=True)


class City(models.Model):
    name_ch = models.CharField(max_length=512, blank=True)
    name_en = models.CharField(max_length=512, blank=True)
    code = models.CharField(max_length=128, blank=True)
    country = models.ForeignKey(to=Country, on_delete=models.CASCADE, related_name='country_city_set', blank=True, null=True)
    province = models.ForeignKey(to=Country, on_delete=models.CASCADE, related_name='province_city_set', blank=True, null=True)
    jingdu = models.FloatField(blank=True, null=True)
    weidu = models.FloatField(blank=True, null=True)
