from django.contrib import admin
#from core.models import Caixa
from .models import(
    Sexo,
    Departamento,
    Funcionario,
    Cliente,
    Fornecedor,
)
admin.site.register(Sexo)
admin.site.register(Departamento)
admin.site.register(Funcionario)
admin.site.register(Cliente)
admin.site.register(Fornecedor)