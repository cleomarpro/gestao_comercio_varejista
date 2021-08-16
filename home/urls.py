from django.urls import  path
from home import views
from .views import (
    Usuario
)

urlpatterns = [
    path('', views.home),
    path('home/', views.home, name='inicio'),
    path('tela_inicial/', views.TelaInicial, name='tela_inicial'),
    path('usuario/', Usuario.as_view(), name='usuario'),
]
