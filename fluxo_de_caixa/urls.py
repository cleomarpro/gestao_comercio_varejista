

from django.urls import path
from .views import (
    NovoPedido, NovoItemPedido, ListaVendas, AtualizarPedido,
    EditPedido, DeletePedido, DeleteItemPedido,
    CaixaDepositar, CaixaSacar, Caixas, ListaVendaPorUsuario, AbrirFeixarCaixa
)


urlpatterns = [
    path('', ListaVendas.as_view(), name='lista-vendas'),
    #path('buscar-produtos', BuscarProduto.as_view(), name='buscar-produtos'),
    path('novo-pedido/', NovoPedido.as_view(), name="novo-pedido"),
    #path('ultimas-pedido/', UltimasVendas.as_view(), name="ultimas-pedido"),
    path('atualizar-pedido/', AtualizarPedido.as_view(), name="atualizar-pedido"),
    path('novo-item-pedido/<int:venda>/', NovoItemPedido.as_view(), name="novo-item-pedido"),
    path('lista-venda-usuario/', ListaVendaPorUsuario.as_view(), name="lista-venda-usuario"),
    path('edit-pedido/<int:venda>/', EditPedido.as_view(), name="edit-pedido"),
    path('delete-item-pedido/<int:item>/', DeleteItemPedido.as_view(), name="delete-item-pedido"),
    #path('excecao/<int:item>/', Excecao.as_view(), name="excecao"),
    path('delete-pedido/<int:venda>/', DeletePedido.as_view(), name="delete-pedido"),
    path('caixa-deposito/<int:id>/', CaixaDepositar.as_view(), name="caixa-deposito"),
    path('caixa-sacar/<int:id>/', CaixaSacar.as_view(), name="caixa-sacar"),
    path('abrir-feixar-caixa/<int:id>/', AbrirFeixarCaixa.as_view(), name="abrir-feixar-caixa"),
    path('caixa/', Caixas.as_view(), name="caixa"),
]

'''
from django.urls import  path
from vendas import views
from .views import (
    ListaVendas,

)

urlpatterns = [
    path('', views.vendas),
    #path('vendas/', views.vendas),
   # path('login/', views.login),


    path('caixa/', ListaVendas.as_view(), name='lista-vendas'),
    path('vendas/', views.vendas, name= 'vendas_listarvendas'),
    path('vendas-update/(?P<id>\d+)/', views.vendas_update, name='vendas_update'),
    path('vendas-novo/', views.vendas_novo, name= 'vendas_novo'),
'''
