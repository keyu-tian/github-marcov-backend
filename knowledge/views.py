import json
from django.views import View
from knowledge.models import Knowledge, EpidemicPolicy
from utils.meta_wrapper import JSR


class KnowledgeList(View):
    @JSR('status', 'data')
    def get(self, request):
        try:
            start = int(request.GET.get('start'))
        except:
            return 1
        res_set = Knowledge.objects.all()[start: start + 12]
        res = [{
            'id': a.id,
            'title': a.title,
            'summary': a.body,
            'source': a.source,
        }for a in res_set]
        return 0, res


class EpidemicNewsList(View):
    @JSR('status', 'data')
    def post(self, request):
        query_set = EpidemicPolicy.objects.all()
        res = []
        for a in query_set:
            res.append({
                'title': a.title,
                'datetime': a.datetime,
                'src': a.src,
                'body': a.body,
            })
        return 0, res
