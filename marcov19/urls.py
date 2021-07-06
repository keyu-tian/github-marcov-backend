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
from django.contrib import admin
from django.urls import path
from train.views import *
from flight.views import *
from risk.views import *
from user.views import *
from epidemic.views import *

urlpatterns = [
    path('/', admin.site.urls),


    path('map/province', MapProvince.as_view()),
    path('map/province_dt', MapProvinceDt.as_view()),



    path('travel/risk_area', RiskAreaList.as_view(), name='risk_area'),
    path('travel/train', TravelTrain.as_view()),
    path('travel/country', CountryFlightInfo.as_view()),
    path('travel/search', TravelSearch.as_view()),



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
]
