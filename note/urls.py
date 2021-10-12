# -*- codeing = utf-8 -*-
# @Time :2021/8/29 20:01
# @Author : 刁雪杭
# @File :urls.py
# @Software:PyCharm
from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_note),
    path('look/',views.look_note),
    path('update/<int:note_id>',views.update_note),
    path('del/',views.del_note)
]
