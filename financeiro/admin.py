from django.contrib import admin
#from core.models import Caixa
from .models import(
    Gastos_extras,
    Tipo_de_conta,
    Contas,
    Pagamento,
    GastosExtrasCategoria,

)

admin.site.register(Gastos_extras)
admin.site.register(Tipo_de_conta)
admin.site.register(Contas)
admin.site.register(Pagamento)
admin.site.register(GastosExtrasCategoria)