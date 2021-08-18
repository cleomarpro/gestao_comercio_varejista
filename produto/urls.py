from django.urls import path
from produto import views
from .views import (
    NovoProduto, ListaProdutos, Categoria_de_produto, FiltroPorCategoria,
    Entrada_Mercadoria , ProdutoUpdate, CategoriaUpdate, entradaMercadoria,
    FiltrarEntadaPorCategoria, NovaPromocao, PromocaoUpdate, ValidadeProdutos,
)
urlpatterns = [
    #path('', ListaVendas.as_view(), name='lista-vendas'),
    path('listar-produto/', ListaProdutos.as_view(), name='listar-produto'),
    path('categoria/', Categoria_de_produto.as_view(), name='categoria'),
    path('entrada-mercadoria/', Entrada_Mercadoria.as_view(), name='entrada-mercadoria'),
    path('validade-produtos/', ValidadeProdutos.as_view(), name='validade-produtos'),
    path('produto/', NovoProduto.as_view(), name="produto"),
    path('promocao/', NovaPromocao.as_view(), name="promocao"),
    path('promocao-update/<int:pk>/', PromocaoUpdate.as_view(), name='promocao-update'),
    path('delete-promocao-confirm/(?P<id>\d+)/', views.promocao_delete, name='promocao_delete'),
    path('produto_update/(?P<id>\d+)/', ProdutoUpdate.as_view(), name='produto_update'),
    path('delete-produto-confirm/(?P<id>\d+)/', views.produto_delete, name='produto_delete'),
    path('categoria_update/<int:pk>/', CategoriaUpdate.as_view(), name='categoria_update_cbv'),
    path('delete-categoria-confirm/(?P<id>\d+)/', views.categoria_delete, name='categoria_delete'),
    path('entradaMercadoria_update/<int:pk>/', entradaMercadoria.as_view(), name='entradaMercadoria_update_cbv'),
    path('entradaMercadoria-delete-confirme/(?P<id>\d+)/', views.entradaMercadoria_delete, name='entradaMercadoria_delete'),
    path('filtro-categoria/', FiltroPorCategoria.as_view(), name='filtro-categoria'),
    path('filtro-categoria-entrada-mercadoria/', FiltrarEntadaPorCategoria.as_view(), name='filtro-categoria-entrada-mercadoria'),
]