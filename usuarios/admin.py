from django.contrib import admin
#from core.models import Caixa
from .models import(
    Usuarios,
    Plano,

)

admin.site.register(Usuarios)
admin.site.register(Plano)