from django.contrib import admin
#from core.models import Caixa
from .models import(
    Categoria,
    Produto,
    EntradaMercadoria,
    SaidaMercadoria,
    Promocao
)

admin.site.register(Categoria)
admin.site.register(Produto)
admin.site.register(EntradaMercadoria)
admin.site.register(SaidaMercadoria)
admin.site.register(Promocao)
