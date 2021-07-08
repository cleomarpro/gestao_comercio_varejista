from django.urls import path
from pessoa import views
from .views import ( NovoFornecedor, FornecedorUpdate, NovoCliente, ClienteUpdate

)


urlpatterns = [
    path('novo-fornecedor/', NovoFornecedor.as_view(), name='novo-fornecedor'),
    path('novo-cliente/', NovoCliente.as_view(), name='novo-cliente'),
    path('cliente-delete-confirme/(?P<id>\d+)/', views.cleinte_delete, name='cliente_delete'),
    path('cliente_update/<int:pk>/', ClienteUpdate.as_view(), name='cliente_update'),
    path('fornecedor-delete-confirme/(?P<id>\d+)/', views.fornecedor_delete, name='fornecedor_delete'),
    path('fornecedor_update/<int:pk>/', FornecedorUpdate.as_view(), name='fornecedor_update'),
]