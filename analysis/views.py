from django.views import View
from django.db.models import Q
from utils.meta_wrapper import JSR
from utils.dict_ch import province_dict_ch
from epidemic.models import HistoryEpidemicData
from analysis.models import ProvinceData
import datetime as dt
import json
import os

epidemic_start_date = dt.date(2021, 7, 1)


class DomesticAnalyze(View):
    @JSR('status', 'data')
    def get(self, request):
        print('start')
        json_path = os.path.join('spiders_data', 'epidemic_domestic_data', 'province.json')
        analysis = json.load(open(json_path, 'r', encoding='utf-8'))
        return 0, analysis
