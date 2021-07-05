from django.views import View
from utils.meta_wrapper import JSR
from risk.models import RiskArea


# 根据城市名字获取该城市风险等级
def get_city_risk_level(name) -> int:
    count = RiskArea.objects.filter(city=name).count()
    return (count+1)//2 if (count+1)//2 <= 5 else 5


# Create your views here.
class RiskAreaList(View):
    @JSR('areas')
    def get(self, request):
        area_list = RiskArea.objects.all()
        areas = []
        for area in area_list:
            areas.append({'province': area.province, 'city': area.city if area.city is not None else '', 'detail': area.address, 'risk': area.level})
        return areas


