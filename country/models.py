from django.db import models


class Country(models.Model):
    name_ch = models.CharField(max_length=512, blank=True)
    name_en = models.CharField(max_length=512, blank=True)
    code = models.CharField(max_length=128, blank=True)


class City(models.Model):
    name_ch = models.CharField(max_length=512, blank=True)
    name_en = models.CharField(max_length=512, blank=True)
    code = models.CharField(max_length=128, blank=True)
    country = models.ForeignKey(to=Country, on_delete=models.CASCADE, related_name='city_set', blank=True, null=True)
