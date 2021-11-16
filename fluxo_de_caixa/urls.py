

from fluxo_de_caixa import views
from django.urls import path
from .views import (
    NovoPedido, NovoItemPedido, ListaVendas, AtualizarPedido, 
    EditPedido, DeletePedido, DeleteItemPedido, ListaVendaPagas,
    CaixaDepositar, CaixaSacar, Caixas, CaixasUpdate,
    ListaVendaPorUsuario, AbrirFeixarCaixa
)


urlpatterns = [
    path('', ListaVendas.as_view(), name='lista-vendas'),
    path('vendas-pagas/', ListaVendaPagas.as_view(), name='vendas_pagas'),
    path('novo-pedido/', NovoPedido.as_view(), name="novo-pedido"),
    path('atualizar-pedido/', AtualizarPedido.as_view(), name="atualizar-pedido"),
    path('novo-item-pedido/<int:venda>/', NovoItemPedido.as_view(), name="novo-item-pedido"),
    path('lista-venda-usuario/', ListaVendaPorUsuario.as_view(), name="lista-venda-usuario"),
    path('edit-pedido/<int:venda>/', EditPedido.as_view(), name="edit-pedido"),
    path('delete-item-pedido/<int:item>/', DeleteItemPedido.as_view(), name="delete-item-pedido"),
    path('delete-pedido/<int:venda>/', DeletePedido.as_view(), name="delete-pedido"),
    path('caixa-deposito/<int:id>/', CaixaDepositar.as_view(), name="caixa-deposito"),
    path('caixa-sacar/<int:id>/', CaixaSacar.as_view(), name="caixa-sacar"),
    path('abrir-feixar-caixa/<int:id>/', AbrirFeixarCaixa.as_view(), name="abrir-feixar-caixa"),
    path('caixa/', Caixas.as_view(), name="caixa"),
    path('caixa-update/<int:id>/', CaixasUpdate.as_view(), name='caixa-update'),
    path('delete-caixa/(?P<id>\d+)/', views.caixa_delete, name='delete-caixa'),
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
