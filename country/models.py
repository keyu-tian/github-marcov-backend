from django.db import models

from utils.cast import decode, encode


class Country(models.Model):
    @staticmethod
    def get_via_encoded_id(encoded_id):
        u = Country.objects.filter(id=int(decode(encoded_id)))
        return u.get() if u.exists() else None

    @property
    def encoded_id(self):
        return encode(self.id)

    name_ch = models.CharField(max_length=512, blank=True)
    name_en = models.CharField(max_length=512, blank=True)
    code = models.CharField(max_length=128, blank=True)


class City(models.Model):
    @staticmethod
    def get_via_encoded_id(encoded_id):
        u = City.objects.filter(id=int(decode(encoded_id)))
        return u.get() if u.exists() else None

    @property
    def encoded_id(self):
        return encode(self.id)

    name_ch = models.CharField(max_length=512, blank=True)
    name_en = models.CharField(max_length=512, blank=True)
    code = models.CharField(max_length=128, blank=True)
    country = models.ForeignKey(to=Country, on_delete=models.CASCADE, related_name='city_set', blank=True, null=True)
