from django.contrib import admin
#from core.models import Caixa
from .models import(
    Categoria,
    Produto,
    EntradaMercadoria,
    Promocao
)

admin.site.register(Categoria)
admin.site.register(Produto)
admin.site.register(EntradaMercadoria)
admin.site.register(Promocao)
