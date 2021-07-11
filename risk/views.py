from django.views import View
from utils.meta_wrapper import JSR
from risk.models import RiskArea


# 根据城市名字获取该城市风险等级
def get_city_risk_level(name) -> int:
    if RiskArea.objects.filter(address__icontains=name, level=2).count() > 0:
        return 4
    elif RiskArea.objects.filter(address__icontains=name, level=1).count() > 0:
        return 3
    return 2


# Create your views here.
class RiskAreaList(View):
    @JSR('status', 'areas')
    def get(self, request):
        area_list = RiskArea.objects.all()
        areas = []
        for area in area_list:
            areas.append({'province': area.province, 'city': area.city if area.city is not None else '', 'detail': area.address, 'risk': area.level})
        return 0, areas


