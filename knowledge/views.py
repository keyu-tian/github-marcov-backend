import json
from django.views import View
from knowledge.models import Knowledge
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
