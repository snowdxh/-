# -*- codeing = utf-8 -*-
# @Time :2021/8/27 21:17
# @Author : 刁雪杭
# @File :urls.py
# @Software:PyCharm
from django.urls import path
from . import views
urlpatterns = [
    path('reg/',views.reg_view),
    path('login/',views.login_view),
    path('logout/',views.logout_view),
]
