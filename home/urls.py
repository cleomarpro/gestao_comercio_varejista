from django.urls import  path
from home import views

urlpatterns = [
    path('', views.home),
    path('home/', views.home, name='inicio'),
    path('tela_inicial/', views.TelaInicial, name='tela_inicial'),
    path('usuario/', views.usuario, name='usuario'),
]
