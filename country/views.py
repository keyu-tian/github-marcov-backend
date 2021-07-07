from django.shortcuts import render
from country.models import *


def get_travel_enter_policy_msg(city):
    # 根据城市（省的下一级）查msg，传入str，返回str
    query_set = Policy.objects.filter(city_name=city)
    if query_set.count() == 1:
        query = query_set.get()
        return f'进入{ query.city_name }：{ query.enter_policy }'
    else:
        return ''


def get_travel_out_policy_msg(city):
    # 根据城市（省的下一级）查msg，传入str，返回str
    query_set = Policy.objects.filter(city_name=city)
    if query_set.count() == 1:
        query = query_set.get()
        return f'离开{ query.city_name }：{ query.out_policy }'
    else:
        return ''