import json

from django.db.models import QuerySet
from django.views import View

from country.models import Policy
from utils.meta_wrapper import JSR


class TravelPolicy(View):
    @JSR('status', 'enter_policy', 'out_policy')
    def post(self, request):
        kwargs: dict = json.loads(request.body)
        if kwargs.keys() != {'city'}:
            return 1, '', ''

        key: str = kwargs['city']
        if key[-1] not in {'省', '市'}:
            key += '市'
        
        query_key = 'city_name' if key[-1] == '市' else 'province_name'
        po_set: QuerySet = Policy.objects.filter(**{query_key: key})
        
        if po_set.count() != 1:
            return 7, '', ''

        try:
            po: Policy = po_set.get()
        except:
            return 2, '', ''
        
        return 0, po.enter_policy, po.out_policy
    