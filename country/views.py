import json

from django.db.models import QuerySet, Q
from django.views import View

from country.models import Policy
from utils.dict_ch import province_capital_city
from utils.meta_wrapper import JSR


class TravelPolicy(View):
    @JSR('status', 'enter_policy', 'out_policy')
    def post(self, request):
        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != {'city'}:
            return 1, '', ''

        key: str = kwargs['city']

        po_set: QuerySet = Policy.objects.filter(city_name=key)
        
        if po_set.count() == 1:
            po: Policy = po_set.get()
            return 0, po.enter_policy, po.out_policy

        po_set: QuerySet = Policy.objects.filter(province_name=key)
        if po_set.count() >= 1:
            po_set = po_set.filter(city_name=province_capital_city[key])
        elif po_set.count() == 0:
            return 7, '', ''
        try:
            po: Policy = po_set.get()
        except:
            return 2, '', ''
        
        return 0, po.enter_policy, po.out_policy
