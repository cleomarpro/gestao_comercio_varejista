from datetime import date
import datetime
from django.contrib.auth.models import User
from django.db.models.aggregates import Count, Sum
from financeiro.models import Contas, Gastos_extras
from fluxo_de_caixa.models import Depositar_sacar, ItemDoPedido, Venda
from pessoa.models import Funcionario, Sexo
from produto.models import EntradaMercadoria
from usuarios.models import Cobranca, Usuarios, Plano
from django.views import View
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin



def registro_de_dados(user):
    usuario_admi = Usuarios.objects.get(id = user)
    usuario_celecionado = usuario_admi.id
    data = {}
    today = date.today()
    ano_atual = today.year
    MES = today.month
    if MES > 1 and MES <= 12:
        mes = MES - 1
    else:
        mes = 12
    dia = today.day
    data_atual= date(day=dia, month=mes, year=ano_atual)
    data_de_vencimento =  str(ano_atual)+'-'+ str(mes)
    if data_de_vencimento !=None:
        data_de_vencimento =  datetime.datetime.strptime(data_de_vencimento, "%Y-%m")
        Mes = data_de_vencimento.month
        ano_atual = data_de_vencimento.year
    if data_de_vencimento != None:
        Mes= mes

        vendas = Venda.objects.filter(
            usuarios_id= usuario_celecionado, data_hora__month= MES, data_hora__year= ano_atual ).aggregate(count= Count('id'))
        vendas = vendas['count'] or 0

        item_do_pedito = ItemDoPedido.objects.filter(
            usuarios_id= usuario_celecionado, venda__data_hora__month= Mes, venda__data_hora__year= ano_atual ).aggregate(count= Count('id'))
        item_do_pedito = item_do_pedito['count'] or 0
        
        Contas_a_receber = Contas.objects.filter(
            usuarios_id= usuario_celecionado, data_hora__month= Mes, tipo_de_conta__id=1, data_hora__year= ano_atual).aggregate(count= Sum('parcelas'))
        Contas_a_receber = Contas_a_receber['count'] or 0

        Contas_a_pagar = Contas.objects.filter(
            usuarios_id= usuario_celecionado, data_hora__month= Mes, tipo_de_conta__id=2, data_hora__year= ano_atual).aggregate(count= Sum('parcelas'))
        Contas_a_pagar = Contas_a_pagar['count'] or 0

        gastos_extras = Gastos_extras.objects.filter(
            usuarios_id= usuario_celecionado, data_hora__month= Mes, data_hora__year= ano_atual).aggregate(count= Count('id'))
        gastos_extras = gastos_extras['count'] or 0

        entrada_de_mercadoria = EntradaMercadoria.objects.filter(
            usuarios_id= usuario_celecionado, data_hora__month= Mes, data_hora__year= ano_atual).aggregate(count= Count('id'))
        entrada_de_mercadoria = entrada_de_mercadoria['count'] or 0

        caixa= Depositar_sacar.objects.filter(
            usuarios_id= usuario_celecionado, data_hora__month= Mes, data_hora__year= ano_atual).aggregate(count= Count('id'))
        caixa = caixa['count'] or 0

        total_de_registros= vendas + item_do_pedito + Contas_a_receber + Contas_a_pagar + entrada_de_mercadoria + gastos_extras + caixa
        
        return total_de_registros


def autenticarAutorizar(user_logado):
    if Funcionario.objects.filter(user_id = user_logado): # verificando se o usuário existe em funcionários
        usuario_cliente= Funcionario.objects.get(user__id = user_logado) # buscado funcionário baseado no usuário logado
        usuario= usuario_cliente.id # Buscando o ID dousuário administrador com base no usuário logado
   
    elif Usuarios.objects.filter(user_id = user_logado):
        usuario_cliente = Usuarios.objects.get(user_id = user_logado) # Buscando usuário administrador com base no usuário logado
        usuario = usuario_cliente.id # Obitendo o id  do usuário administrador
    
    if usuario:
        return usuario
    else:
        return None
 

def autorizarcao_de_reistro(usuario_cliente):
    usuario_cliente_admin = Usuarios.objects.get(id = usuario_cliente)
    usuario_plano = usuario_cliente_admin.plano.registro
    total_de_registros = registro_de_dados(usuario_cliente)
    if float(usuario_plano) < total_de_registros:
        return redirect('usuarios')
