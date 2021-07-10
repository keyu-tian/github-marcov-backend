from django.db import models


class Country(models.Model):
    name_ch = models.CharField(primary_key=True, unique=True, db_index=True, max_length=128, blank=True)
    name_en = models.CharField(max_length=512, blank=True)
    code = models.CharField(max_length=128, blank=True)


class Province(models.Model):
    name_ch = models.CharField(primary_key=True, unique=True, db_index=True, max_length=128, blank=True)
    name_en = models.CharField(max_length=512, blank=True)
    country = models.ForeignKey(to=Country, on_delete=models.CASCADE, related_name='province_set', blank=True, null=True)


class City(models.Model):
    name_ch = models.CharField(primary_key=True, unique=True, db_index=True, max_length=128, blank=True)
    name_en = models.CharField(max_length=512, blank=True)
    country = models.ForeignKey(to=Country, on_delete=models.CASCADE, related_name='country_city_set', blank=True, null=True)
    province = models.ForeignKey(to=Province, on_delete=models.CASCADE, related_name='province_city_set', blank=True, null=True)
    jingdu = models.FloatField(blank=True, null=True)
    weidu = models.FloatField(blank=True, null=True)


class Policy(models.Model):
    city = models.ForeignKey(to=City, on_delete=models.DO_NOTHING, related_name='policy_set', blank=True, null=True)
    province = models.ForeignKey(to=Province, on_delete=models.DO_NOTHING, related_name='policy_set', blank=True, null=True)
    city_name = models.CharField(max_length=128, blank=True, null=True)
    province_name = models.CharField(max_length=128, blank=True, null=True)
    enter_policy = models.TextField(blank=True, null=True)
    out_policy = models.TextField(blank=True, null=True)
