'''
from django.urls import  path
from home import views

urlpatterns = [

    path('', views.vieworld),
    path('gestao_vieworld/', views.vieworld, name='inicio'),
]
'''