

from django.urls import path
from usuarios import views
from .views import (
    NovoUsuario, NovoFuncionario, UpdateFuncionario, 
    UpdateUsuario, Cobrancas, Usuario, CobrancaUpdate, Plano
)

urlpatterns = [
    path('novo-usuario', NovoUsuario.as_view(), name='novo-usuario'),
    path('novo-funcionario', NovoFuncionario.as_view(), name='novo-funcionario'),
    path('update-funcionario/(?P<id>\d+)/', UpdateFuncionario.as_view(), name='update-funcionario'),
    path('delete-funcionario/(?P<id>\d+)/', views.funcionarioDelete, name='delete-funcionario'),
    path('update-usuario/', UpdateUsuario.as_view(), name='update-usuario'),
    path('cobranca/(?P<id>\d+)/', Cobrancas.as_view(), name='cobranca'),
    path('usuarios', Usuario.as_view(), name='usuarios'),
    path('cobranca-update/(?P<id>\d+)/', CobrancaUpdate.as_view(), name='cobranca-update'),
    path('plano', Plano.as_view(), name='plano'),
]