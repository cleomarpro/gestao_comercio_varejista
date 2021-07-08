from django.contrib import admin
from .models import Venda
from .models import ItemDoPedido
from .models import Tipo_de_pagamento
from .models import Caixa
from .models import Depositar_sacar
#from .actions import nfe_emitida, nfe_nao_emitida


class ItemPedidoInline(admin.TabularInline):
    model = ItemDoPedido
    extra = 1


class VendaAdmin(admin.ModelAdmin):
   # readonly_fields = ('valor',)
    #autocomplete_fields = ("cliente",)
   #list_filter = ('desconto')
    list_display = ('id', 'valor','desconto','total_desconto', 'finalizada' ,'valor_recebido', 'troco')
    #search_fields = ('id', 'cliente__nome')
   # actions = [nfe_emitida, nfe_nao_emitida]
    inlines = [ItemPedidoInline]

    def total(self, obj):
        return obj.get_total()

 #   total.short_description = 'Total'


admin.site.register(Venda, VendaAdmin)
admin.site.register(ItemDoPedido)
admin.site.register(Tipo_de_pagamento)
admin.site.register(Caixa)
admin.site.register(Depositar_sacar)
