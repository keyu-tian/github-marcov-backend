from django.views import View
from utils.meta_wrapper import JSR
from risk.models import RiskArea


# Create your views here.
class RiskAreaList(View):
    @JSR('areas')
    def get(self, request):
        area_list = RiskArea.objects.all()
        areas = []
        for area in area_list:
            areas.append({'province': area.province, 'city': area.city if area.city is not None else '', 'detail': area.address, 'risk': area.level})
        return areas
