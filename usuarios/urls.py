

from django.urls import path
from usuarios import views
from .views import (
    NovoUsuario, NovoFuncionario, UpdateFuncionario
)

urlpatterns = [
    path('novo-usuario', NovoUsuario.as_view(), name='novo-usuario'),
    path('novo-funcionario', NovoFuncionario.as_view(), name='novo-funcionario'),
    path('update-funcionario/(?P<id>\d+)/', UpdateFuncionario.as_view(), name='update-funcionario'),
    path('delete-funcionario/(?P<id>\d+)/', views.funcionarioDelete, name='delete-funcionario'),
]
