

from django.urls import path
from .views import (
    NovoUsuario, NovoFuncionario
)


urlpatterns = [
    path('novo-usuario', NovoUsuario.as_view(), name='novo-usuario'),
    path('novo-funcionario', NovoFuncionario.as_view(), name='novo-funcionario'),

]
