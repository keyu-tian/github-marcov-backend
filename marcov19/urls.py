"""marcov19 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.views.generic import TemplateView
from django.views.static import serve
from django.urls import path, re_path

from country.views import TravelPolicy
from train.views import *
from flight.views import *
from risk.views import *
from user.views import *
from news.views import *
from epidemic.views import *
from analysis.views import *

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    
    # ======== 一、全局 ========
    path('time', TimeInfo.as_view()),
    
    # ======== 二、地图分析 ========
    path('map/province', MapProvince.as_view()),
    path('map/province_dt', MapProvinceDt.as_view()),
    path('map/oversea', MapOversea.as_view()),
    path('map/oversea_dt', MapOverseaDt.as_view()),
    
    # ======== 三、数据分析 ========
    path('data/international_analyze', InternationalAnalyze.as_view()),
    path('data/today/international_analyze', InternationalTodayAnalyze.as_view()),
    path('data/domestic_analyze', DomesticAnalyze.as_view()),
    path('data/today/domestic_analyze', DomesticTodayAnalyze.as_view()),
    path('data/search', SearchAnalyse.as_view()),
    path('data/country_analyze', CountryAnalyze.as_view()),
    
    # ======== 四、出行 ========
    path('travel/risk_area', RiskAreaList.as_view(), name='risk_area'),
    path('travel/search', TravelSearch.as_view()),
    path('travel/train', TravelTrain.as_view()),
    path('travel/plane_info', TravelPlane.as_view()),
    # path('travel/city', ?.as_view()), # todo
    path('travel/country', CountryFlightInfo.as_view()),
    path('travel/policy', TravelPolicy.as_view()),
    
    # ======== 五、新闻 ========
    path('news/weekly', WeeklyNews.as_view()),
    
    # ======== 六、小知识 ========
    # todo：小知识
    

    # ======== 七、用户系统 ========
    path('account/login', Login.as_view()),
    path('account/register', Register.as_view()),
    path('account/forget_pwd_send', ForgetPwdSend.as_view()),
    path('account/forget_pwd_change', ForgetPwdChange.as_view()),
    path('account/logout', Logout.as_view()),
    path('account/send_ver', SendVer.as_view()),
    path('account/change_pwd', ChangePwd.as_view()),
    path('account/change_info', ChangeInfo.as_view()),
    path('user_info', UserInfo.as_view()),
    path('identity', Identity.as_view()),
    path('upload_pic', UploadPic.as_view()),
    
    # ======== 八、论坛 ========
    # todo：论坛
    

    url(r'^', TemplateView.as_view(template_name='index.html')),
    re_path(r'^upload(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}, name='media')
]
