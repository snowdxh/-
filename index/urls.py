# -*- codeing = utf-8 -*-
# @Time :2021/8/27 22:51
# @Author : 刁雪杭
# @File :urls.py
# @Software:PyCharm
from django.urls import path
from . import views
urlpatterns = [
    path('',views.index_view),
]
