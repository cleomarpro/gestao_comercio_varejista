from django.urls import path
from financeiro import views
from .views import ( GastosExtras, GastosExtrasUpdate, ContasApagar, ContaAreceberUpdate,
Relarorio_produtos, Relatorio_diario, Relatorio_mensal, Relatorio_anual,
FiltroGastosExtras, ContasAreceber, ContaApagarUpdate, Pagamentos, Fatura
)


urlpatterns = [
    path('gastos-extras/', GastosExtras.as_view(), name='gastos-extras'),
    path('gastos-extras-delete-confirme/(?P<id>\d+)/', views.gastosExtras_delete, name='gastos_extras_delete'),
    path('gastos_extras_update/<int:id>/', GastosExtrasUpdate.as_view(), name='gastos_extras_update'),
    path('conta-apagar/', ContasApagar.as_view(), name='conta_apagar'),
    path('pagamento/<int:id>/', Pagamentos.as_view(), name='pagamento'),
    path('conta-areceber/', ContasAreceber.as_view(), name='conta_areceber'),
    path('conta-delete-confirme/(?P<id>\d+)/', views.conta_delete, name='conta_delete'),
    path('conta-apagar-delete/(?P<id>\d+)/', views.conta_apagar_delete, name='conta_apagar_delete'),
    path('conta_areceber_update/<int:id>/', ContaAreceberUpdate.as_view(), name='conta_areceber_update'),
    path('conta_apagar_update/<int:id>/', ContaApagarUpdate.as_view(), name='conta_apagar_update'),
    path('relatorio-produtos/', Relarorio_produtos.as_view(), name='relatorio-produtos'),
    path('relatorio-diario/', Relatorio_diario.as_view(), name='relatorio_diario'),
    path('relatorio-mensal/', Relatorio_mensal.as_view(), name='relatorio_mensal'),
    path('relatorio-anual/', Relatorio_anual.as_view(), name='relatorio_anual'),
    path('fatura/', Fatura.as_view(), name='fatura'),
    path('filtro-gastos-extras/', FiltroGastosExtras.as_view(), name='filtro_gastos_extras'),
]