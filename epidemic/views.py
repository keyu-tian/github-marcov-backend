from django.views import View
from utils.meta_wrapper import JSR
from risk.views import get_city_risk_level
from epidemic.models import HistoryEpidemicData
import json


class MapProvince(View):
    @JSR('status', 'province')
    def post(self, request):
        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != {'name', 'date'}:
            return 1, []
        province = {}
        data = HistoryEpidemicData.objects.filter(date=kwargs['date'], province_ch=kwargs['name'])
        if data.count() == 0:
            return 6, province
        province_data = data.first()
        province['new'] = {
            'died': province_data.province_new_died if province_data.province_new_died else 0,
            'cured': province_data.province_new_cured if province_data.province_new_cured else 0,
            'confirmed': province_data.province_new_confirmed if province_data.province_new_confirmed else 0
        }
        province['total'] = {
            'died': province_data.province_total_died if province_data.province_total_died else 0,
            'cured': province_data.province_total_cured if province_data.province_total_cured else 0,
            'confirmed': province_data.province_total_confirmed if province_data.province_total_confirmed else 0
        }
        cities = []
        infos = []
        for city_data in data:
            info = {'level': get_city_risk_level(city_data.city_ch), 'msg': '未知'}
            city = {'name': city_data.city_ch}
            city['new'] = {
                'died': city_data.city_new_died if city_data.city_new_died else 0,
                'cured': city_data.city_new_cured if city_data.city_new_cured else 0,
                'confirmed': city_data.city_new_confirmed if city_data.city_new_confirmed else 0
            }
            city['total'] = {
                'died': city_data.city_total_died if city_data.city_total_died else 0,
                'cured': city_data.city_total_cured if city_data.city_total_cured else 0,
                'confirmed': city_data.city_total_confirmed if city_data.city_total_confirmed else 0,
            }
            cities.append(city)
            infos.append(info)
        province['cities'] = cities
        province['info'] = infos
        return 0, province


class MapProvinceDt(View):
    @JSR('status', 'data')
    def post(self, request):
        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != {'name'}:
            return 1, []
        total_data = HistoryEpidemicData.objects.filter(province_ch=kwargs['name'])
        res = []
        date = []
        for province_data in total_data:
            if province_data.date in date:
                continue
            data = {'date': province_data.date}
            date.append(province_data.date)
            data['new'] = {
                'died': province_data.province_new_died if province_data.province_new_died else 0,
                'cured': province_data.province_new_cured if province_data.province_new_cured else 0,
                'confirmed': province_data.province_new_confirmed if province_data.province_new_confirmed else 0
            }
            data['total'] = {
                'died': province_data.province_total_died if province_data.province_total_died else 0,
                'cured': province_data.province_total_cured if province_data.province_total_cured else 0,
                'confirmed': province_data.province_total_confirmed if province_data.province_total_confirmed else 0
            }
            res.append(data)
        return 0, res
