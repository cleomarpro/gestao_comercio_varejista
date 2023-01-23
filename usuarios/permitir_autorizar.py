from datetime import date
import datetime
from django.db.models.aggregates import Count, Sum
from financeiro.models import Contas, Gastos_extras
from fluxo_de_caixa.models import Depositar_sacar, ItemDoPedido, Venda
from pessoa.models import Funcionario
from produto.models import EntradaMercadoria
from usuarios.models import Usuarios
from django.shortcuts import redirect

today = date.today()
def registro_de_dados(user, mes = today.month, ano_atual = today.year):
    usuario_celecionado = user

    vendas = Venda.objects.filter(
        usuarios_id= usuario_celecionado, data_hora__month= mes, data_hora__year= ano_atual ).aggregate(count= Count('id'))
    vendas = vendas['count'] or 0

    item_do_pedito = ItemDoPedido.objects.filter(
        usuarios_id= usuario_celecionado, venda__data_hora__month= mes, venda__data_hora__year= ano_atual ).aggregate(count= Count('id'))
    item_do_pedito = item_do_pedito['count'] or 0
    
    Contas_a_receber = Contas.objects.filter(
        usuarios_id= usuario_celecionado, data_hora__month= mes, tipo_de_conta__id=1, data_hora__year= ano_atual).aggregate(count= Sum('parcelas'))
    Contas_a_receber = Contas_a_receber['count'] or 0

    Contas_a_pagar = Contas.objects.filter(
        usuarios_id= usuario_celecionado, data_hora__month= mes, tipo_de_conta__id=2, data_hora__year= ano_atual).aggregate(count= Sum('parcelas'))
    Contas_a_pagar = Contas_a_pagar['count'] or 0

    gastos_extras = Gastos_extras.objects.filter(
        usuarios_id= usuario_celecionado, data_hora__month= mes, data_hora__year= ano_atual).aggregate(count= Count('id'))
    gastos_extras = gastos_extras['count'] or 0

    entrada_de_mercadoria = EntradaMercadoria.objects.filter(
        usuarios_id= usuario_celecionado, data_hora__month= mes, data_hora__year= ano_atual).aggregate(count= Count('id'))
    entrada_de_mercadoria = entrada_de_mercadoria['count'] or 0

    caixa= Depositar_sacar.objects.filter(
        usuarios_id= usuario_celecionado, data_hora__month= mes, data_hora__year= ano_atual).aggregate(count= Count('id'))
    caixa = caixa['count'] or 0

    total_de_registros= vendas + item_do_pedito + Contas_a_receber + Contas_a_pagar + entrada_de_mercadoria + gastos_extras + caixa
    
    return total_de_registros

    
def autenticar_usuario(user_logado):
    if Funcionario.objects.filter(user_id = user_logado): # verificando se o usuário existe em funcionários
        usuario_cliente= Funcionario.objects.get(user_id = user_logado) # buscado funcionário baseado no usuário logado
        usuario= usuario_cliente.usuarios.id # Buscando o ID dousuário administrador com base no usuário logado
   
    elif Usuarios.objects.filter(user_id = user_logado):
        usuario_cliente = Usuarios.objects.get(user_id = user_logado) # Buscando usuário administrador com base no usuário logado
        usuario = usuario_cliente.id # Obitendo o id  do usuário administrador
    
    if usuario:
        return usuario
  
def autorizarcao_de_reistro(usuario_cliente):
    usuario_cliente_admin = Usuarios.objects.get(id = usuario_cliente)
    usuario_plano = usuario_cliente_admin.plano.registro
    total_de_registros = registro_de_dados(usuario_cliente)
    if float(usuario_plano) < total_de_registros:
        return redirect('plano')

def fatura():
    today = date.today()
    mes = today.month
    if mes > 1 and mes <= 12:
        um_mes_atras = mes - 1
    else:
        um_mes_atras = 12
    
    return um_mes_atras