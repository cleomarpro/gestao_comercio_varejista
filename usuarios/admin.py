from django.contrib import admin
#from core.models import Caixa
from .models import(
    Usuarios,
    Plano,
    Cobranca,

)

admin.site.register(Usuarios)
admin.site.register(Plano)
admin.site.register(Cobranca)