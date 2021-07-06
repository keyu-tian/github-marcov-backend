from django.db import models


# Create your models here.
class ProvinceData(models.Model):
    province_ch = models.CharField(max_length=512, blank=True)
    # province_en = models.CharField(max_length=512, blank=True)
    population = models.IntegerField(blank=True, null=True)

