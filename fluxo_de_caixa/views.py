#from django.shortcuts import render
from datetime import date
from django.contrib.auth.decorators import login_required
#import datetime
#from django.db.models import Sum, Count, F #Avg ,DecimalField, F # Max ExpressionWrapper FloatField DecimalField Sum
#from django.core.exceptions import ValidationError
#from django import forms
#from django.contrib.auth import authenticate
#from django.http import HttpResponse
from django.shortcuts import render, redirect
#from django.contrib.auth.decorators import login_required
from django.views import View
from .models import Venda, Depositar_sacar, Caixa
from .models import Produto
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from usuarios.models import Usuarios
from pessoa.models import Fornecedor, Funcionario
from django.db.models import Sum 
from django.db.models import Q
#from django.contrib.auth.models import User
#from django.contrib.auth.decorators import login_required
#from financeiro.models import Contas
#from financeiro.models import Gastos_extras
#from pessoa.models import pessoaFisica
from .models import ItemDoPedido
#from .forms import ItemPedidoForm #produtoForm

class AtualizarPedido(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user.has_perm('fluxo_de_caixa.change_venda')
        if user == False:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

        return render(
            request, 'novo-pedido.html')
    def post(self, request):
        user = request.user.has_perm('fluxo_de_caixa.change_venda')
        if user == False:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        
        data = {}
        user_logado = request.user # Obitendo o usuário logado
        user_logado = user_logado.id # obitendo o ID do usuário logado
        if Funcionario.objects.filter(user_id = user_logado): # verificando se o usuário existe em funcionários
            funcionario= Funcionario.objects.get(user__id = user_logado) # buscado funcionário baseado no usuário logado
            usuario= funcionario.usuarios.id # Buscando o ID dousuário administrador com base no usuário logado
            usuarios = Usuarios.objects.get(id = usuario) # Buscando usuário administrador com base no usuário logado
        else:
            usuarios = Usuarios.objects.get(user_id = user_logado) # Buscando usuário administrador com base no usuário logado
            usuario = usuarios.id # Obitendo o id  do usuário administrador

        data['pagamento']= request.POST['pagamento']  or 1
        data['descricao']= request.POST['descricao']
        data['valor_recebido']= request.POST['valor_recebido']
        data['valor_credito']= request.POST['valor_credito']
        data['valor_debito']= request.POST['valor_debito']
        data['finalizada']= request.POST.get('finalizada', False)
        data['desconto'] = request.POST['desconto']
        data['venda_id'] = request.POST['venda_id']
        
        if data['venda_id']:
            vendas= Venda.objects.get(id= request.POST['venda_id'])
            usuario_adm = vendas.usuarios.id

            if usuario_adm == usuario:
                venda = Venda.objects.get(id=data['venda_id'])
                venda.desconto = data['desconto'].replace(',', '.').replace('%', '') or 0
                venda.tipo_de_pagamento_id = data['pagamento'] or 1
                venda.finalizada = data['finalizada']
                venda.descricao = data['descricao']
                venda.valor_recebido = data['valor_recebido'].replace('.','').replace(',','.').replace('R$\xa0','').replace('R$','')
                venda.valor_credito = data['valor_credito'].replace('.','').replace(',','.').replace('R$\xa0','').replace('R$','')
                venda.valor_debito = data['valor_debito'].replace('.','').replace(',','.').replace('R$\xa0','').replace('R$','')
                venda.user_2 = user_logado
                venda.venda_id = data['venda_id']

                venda.save()
            
            else:
                return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        else:
            user = request.user.has_perm('fluxo_de_caixa.add_venda')
            if user == False:
                return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

            venda = Venda.objects.create(user = user_logado, usuarios_id = usuario)

        itens = venda.itemdopedido_set.all().order_by('-id')
        data['venda'] = venda
        data['itens'] = itens
        data['usuarios'] = usuarios
        return render(
            request, 'novo-pedido.html', data)

class NovoPedido(LoginRequiredMixin, View):

    def post(self, request):
        user = request.user.has_perm('fluxo_de_caixa.add_venda')
        if user == False:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

        user_logado = request.user # Obitendo o usuário logado
        user_logado = user_logado.id # obitendo o ID do usuário logado
        if Funcionario.objects.filter(user_id = user_logado): # verificando se o usuário existe em funcionários
            funcionario= Funcionario.objects.get(user__id = user_logado) # buscado funcionário baseado no usuário logado
            usuario= funcionario.usuarios.id # Buscando o ID dousuário administrador com base no usuário logado
            usuarios = Usuarios.objects.get(id = usuario) # Buscando usuário administrador com base no usuário logado
        else:
            usuarios = Usuarios.objects.get(user_id = user_logado) # Buscando usuário administrador com base no usuário logado
            usuario = usuarios.id # Obitendo o id  do usuário administrador

        data = {}
        data['venda_id'] = request.POST['venda_id']

        venda = Venda.objects.create(user = user_logado, usuarios_id = usuario)

        itens = venda.itemdopedido_set.all().order_by('-id')
        data['venda'] = venda
        data['itens'] = itens
        data['usuarios'] = usuarios
        return render(
            request, 'novo-pedido.html', data)

class NovoItemPedido(LoginRequiredMixin, View):

    def get(self, request):
        user = request.user.has_perm('fluxo_de_caixa.add_venda')
        if user == False:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

        pass

    def post(self, request, venda):
        user = request.user.has_perm('fluxo_de_caixa.add_venda')
        if user == False:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        data = {}

        user_logado = request.user # Obitendo o usuário logado
        user_logado = user_logado.id # obitendo o ID do usuário logado
        if Funcionario.objects.filter(user_id = user_logado): # verificando se o usuário existe em funcionários
            funcionario= Funcionario.objects.get(user__id = user_logado) # buscado funcionário baseado no usuário logado
            usuarioId= funcionario.usuarios.id # Buscando o ID dousuário administrador com base no usuário logado
            usuarioCliente= funcionario.usuarios.usuario_cliente # Buscando o ID dousuário administrador com base no usuário logado
            usuarios = Usuarios.objects.get(id = usuarioId) # Buscando usuário administrador com base no usuário logado
        else:
            usuarios = Usuarios.objects.get(user_id = user_logado) # Buscando usuário administrador com base no usuário logado
            usuarioId = usuarios.id # Obitendo o id  do usuário administrador
            usuarioCliente= usuarios.usuario_cliente # Obitendo o id  do usuário_cliente administrador

        produto= Produto.objects.filter(usuarios__usuario_cliente= usuarioCliente, codigo= request.POST['produto_codigo'] ) or 0
        if produto != 0:
            produto_id= produto.latest('pk').pk
        if produto == 0:
            data['mensagen_de_erro'] = 'Produto não cadastrado!'
            venda = Venda.objects.get(id=venda)
            data['venda'] = venda
            data['itens'] = venda.itemdopedido_set.all()
            return render(
                request, 'novo-pedido.html', data)

        else:
            item = ItemDoPedido.objects.create(
                produto_id = produto_id,
                quantidade_de_itens=request.POST['quantidade'].replace(',', '.') or 1,
                estoque_fisico_atual=request.POST['estoque_fisico_atual'] or 0,
                desconto=request.POST['desconto'].replace(',', '.') or 0,
                venda_id=venda, user = user_logado, usuarios_id = usuarioId)

            data['venda'] = item.venda
            data['itens'] = item.venda.itemdopedido_set.all().order_by('-id')
            data['usuarios'] = usuarios
            return render(
                request, 'novo-pedido.html', data)

class SaidaDeMercadoria(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user.has_perm('fluxo_de_caixa.add_venda')
        if user == False:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        else:
            return render(
                request, 'saida_mercadoria.html')

    def post(self, request):
        user = request.user.has_perm('fluxo_de_caixa.add_venda')
        if user == False:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        data = {}

        user_logado = request.user # Obitendo o usuário logado
        user_logado = user_logado.id # obitendo o ID do usuário logado
        if Funcionario.objects.filter(user_id = user_logado): # verificando se o usuário existe em funcionários
            funcionario= Funcionario.objects.get(user__id = user_logado) # buscado funcionário baseado no usuário logado
            usuarioId= funcionario.usuarios.id # Buscando o ID dousuário administrador com base no usuário logado
            usuarioCliente= funcionario.usuarios.usuario_cliente # Buscando o ID dousuário administrador com base no usuário logado
            usuarios = Usuarios.objects.get(id = usuarioId) # Buscando usuário administrador com base no usuário logado
        else:
            usuarios = Usuarios.objects.get(user_id = user_logado) # Buscando usuário administrador com base no usuário logado
            usuarioId = usuarios.id # Obitendo o id  do usuário administrador
            usuarioCliente= usuarios.usuario_cliente # Obitendo o id  do usuário_cliente administrador
            
        produto= Produto.objects.filter(
            usuarios__usuario_cliente= usuarioCliente, codigo= request.POST['produto_codigo'] ) or 0
        if produto != 0:
            produto_id= produto.latest('pk').pk
        if produto == 0:
            data['mensagen_de_erro'] = 'Produto não cadastrado!'
            data['mensagen_de_erro_dica'] = 'Verifica o cdigo e tente novamente!' 
            data['mensagen_de_erro_acao'] = 'Para feichar, pressione ( Alt + X ) !'
            return render(
                request, 'saida_mercadoria.html', data)
        else:
            produtoestoque= Produto.objects.get(codigo = request.POST['produto_codigo'])
            produto_estoque =  produtoestoque.estoque
            if float(produto_estoque) < float(request.POST['estoque_fisico_atual']):
                data['mensagen_de_erro_2'] = 'Estoque menor que a quantidade inserida!'
                data['mensagen_de_erro_dica'] = 'Seu estoque deve está desatualizado, atualize-o e tente novamente!' 
                data['mensagen_de_erro_acao'] = 'Para feichar, pressione ( Alt + X ) !'
                return render(
                request, 'saida_mercadoria.html', data)
            else:
                venda = Venda.objects.create(user = user_logado, usuarios_id = usuarioId)
                item = ItemDoPedido.objects.create(
                    produto_id = produto_id,
                    estoque_fisico_atual=request.POST['estoque_fisico_atual'],
                    venda_id=venda.id, user = user_logado, usuarios_id = usuarioId)
                    
                data['saida'] = ItemDoPedido.objects.get(id=item.id)
                return render(
                    request, 'saida_mercadoria.html', data)

class ListaVendas(LoginRequiredMixin, View):
    def get(self, request):
        data = {}

        user = request.user.has_perm('fluxo_de_caixa.view_venda')
        if user == False:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

        user_logado = request.user # Obitendo o usuário logado
        user_logado = user_logado.id # obitendo o ID do usuário logado
        if Funcionario.objects.filter(user_id = user_logado): # verificando se o usuário existe em funcionários
            funcionario= Funcionario.objects.get(user__id = user_logado) # buscado funcionário baseado no usuário logado
            usuario= funcionario.usuarios.usuario_cliente # Buscando o ID dousuário administrador com base no usuário logado
        else:
            usuario = Usuarios.objects.get(user_id = user_logado) # Buscando usuário administrador com base no usuário logado
            usuario = usuario.usuario_cliente # Obitendo o id  do usuário administrador
        today = date.today()

        Mes= request.GET.get('mes',None)
        busca= request.GET.get('venda',None)
        Dia= request.GET.get('dia',None)

        vendas = Venda.objects.filter(
            data_hora__gte=today, usuarios__usuario_cliente= usuario).order_by('-id') #__startswith, __contains
        if Dia:
            vendas = Venda.objects.filter(data_hora__contains=Dia, usuarios__usuario_cliente= usuario).order_by('-id')#data_hora__day= Dia
        if Mes:
            vendas = Venda.objects.filter(
                data_hora__year__contains=today.year, data_hora__month__contains=Mes, usuarios__usuario_cliente= usuario ).order_by('-id')
        if busca:
            vendas = Venda.objects.filter( usuarios__usuario_cliente= usuario, id__icontains=busca)
        data['vendas'] = vendas
        return render(request, 'lista-vendas.html', data)


class ListaVendaPorUsuario(LoginRequiredMixin, View):
    def get(self, request):
        data = {}

        user = request.user.has_perm('fluxo_de_caixa.view_venda')
        if user == False:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

        user_logado = request.user # Obitendo o usuário logado
        user_logado = user_logado.id # obitendo o ID do usuário logado
        if Funcionario.objects.filter(user_id = user_logado): # verificando se o usuário existe em funcionários
            funcionario= Funcionario.objects.get(user__id = user_logado) # buscado funcionário baseado no usuário logado
            usuario= funcionario.usuarios.usuario_cliente # Buscando o ID dousuário administrador com base no usuário logado
        else:
            usuario = Usuarios.objects.get(user_id = user_logado) # Buscando usuário administrador com base no usuário logado
            usuario = usuario.usuario_cliente # Obitendo o id  do usuário administrador
        today = date.today()

        Mes= request.GET.get('mes',None)
        busca= request.GET.get('venda',None)
        Dia= request.GET.get('dia',None)

        vendas = Venda.objects.filter(
            data_hora__gte=today, user = user_logado, usuarios__usuario_cliente= usuario).order_by('-id') #__startswith, __contains
        total_vendas= vendas.aggregate(total=Sum("valor_com_desconto"))
        total_desconto= vendas.aggregate(total=Sum("total_desconto"))
        if Dia:
            vendas = Venda.objects.filter(
                data_hora__contains=Dia, user = user_logado, usuarios__usuario_cliente= usuario).order_by('-id')#data_hora__day= Dia
            total_vendas= vendas.aggregate(total=Sum("valor_com_desconto"))
            total_desconto= vendas.aggregate(total=Sum("total_desconto"))
        if Mes:
            vendas = Venda.objects.filter(
                data_hora__year__contains=today.year, data_hora__month__contains=Mes, user = user_logado, usuarios__usuario_cliente= usuario ).order_by('-id')
            total_vendas= vendas.aggregate(total=Sum("valor_com_desconto"))
            total_desconto= vendas.aggregate(total=Sum("total_desconto"))

        if busca:
            vendas = Venda.objects.filter(
                user = user_logado, usuarios__usuario_cliente= usuario, id__icontains=busca)
            total_vendas= vendas.aggregate(total=Sum("valor_com_desconto"))
            total_desconto= vendas.aggregate(total=Sum("total_desconto"))
        data['vendas'] = vendas
        data['total_vendas']= total_vendas
        data['total_desconto']= total_desconto
        return render(request, 'lista-venda-usuario.html', data)

class ListaVendaPagas(LoginRequiredMixin, View):
    def get(self, request):
        data = {}

        user = request.user.has_perm('fluxo_de_caixa.view_venda')
        if user == False:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

        user_logado = request.user # Obitendo o usuário logado
        user_logado = user_logado.id # obitendo o ID do usuário logado
        if Funcionario.objects.filter(user_id = user_logado): # verificando se o usuário existe em funcionários
            funcionario= Funcionario.objects.get(user__id = user_logado) # buscado funcionário baseado no usuário logado
            usuario= funcionario.usuarios.usuario_cliente # Buscando o ID dousuário administrador com base no usuário logado
        else:
            usuario = Usuarios.objects.get(user_id = user_logado) # Buscando usuário administrador com base no usuário logado
            usuario = usuario.usuario_cliente # Obitendo o id  do usuário administrador
        today = date.today()

        Mes= request.GET.get('mes',None)
        busca= request.GET.get('venda',None)
        Dia= request.GET.get('dia',None)

        vendas = Venda.objects.filter(
            data_hora__gte=today, user_2 = user_logado, usuarios__usuario_cliente= usuario).order_by('-id') #__startswith, __contains
        total_vendas= vendas.aggregate(total=Sum("valor_com_desconto"))

        if Dia:
            vendas = Venda.objects.filter(
                data_hora__contains=Dia, user_2 = user_logado, usuarios__usuario_cliente= usuario).order_by('-id')#data_hora__day= Dia
            total_vendas= vendas.aggregate(total=Sum("valor_com_desconto"))

        if Mes:
            vendas = Venda.objects.filter(
                data_hora__year__contains=today.year, data_hora__month__contains=Mes, user_2 = user_logado, usuarios__usuario_cliente= usuario ).order_by('-id')
            total_vendas= vendas.aggregate(total=Sum("valor_com_desconto"))

        if busca:
            vendas = Venda.objects.filter(
                user_2 = user_logado, usuarios__usuario_cliente= usuario, id__icontains=busca)
            total_vendas= vendas.aggregate(total=Sum("valor_com_desconto"))
            
        data['vendas'] = vendas
        data['total_vendas']= total_vendas
        return render(request, 'vendas-pagas.html', data)

class EditPedido(LoginRequiredMixin, View):
    def get(self, request, venda):
        user = request.user.has_perm('fluxo_de_caixa.view_venda')
        if user == False:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        
        user_logado = request.user # Obitendo o usuário logado
        user_logado = user_logado.id # obitendo o ID do usuário logado
        if Funcionario.objects.filter(user_id = user_logado): # verificando se o usuário existe em funcionários
            funcionario= Funcionario.objects.get(user__id = user_logado) # buscado funcionário baseado no usuário logado
            usuario= funcionario.usuarios.id # Buscando o ID dousuário administrador com base no usuário logado
            usuarios = Usuarios.objects.get(id = usuario)
        else:
            usuarios = Usuarios.objects.get(user_id = user_logado) # Buscando usuário administrador com base no usuário logado
            usuario = usuarios.id # Obitendo o id  do usuário administrador

        data = {}
        venda = Venda.objects.get(id=venda)
        usuario_adm = venda.usuarios.id
        if usuario_adm == usuario:
            data['venda'] = venda
            data['itens'] = venda.itemdopedido_set.all()
            data['usuarios'] = usuarios
            return render(
                request, 'novo-pedido.html', data)
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        
class DeletePedido(LoginRequiredMixin, View):
    def get(self, request, venda):
        user = request.user.has_perm('fluxo_de_caixa.delete_venda')
        if user == False:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        user_logado = request.user # Obitendo o usuário logado
        user_logado = user_logado.id # obitendo o ID do usuário logado
        if Funcionario.objects.filter(user_id = user_logado): # verificando se o usuário existe em funcionários
            funcionario= Funcionario.objects.get(user__id = user_logado) # buscado funcionário baseado no usuário logado
            usuario= funcionario.usuarios.id # Buscando o ID dousuário administrador com base no usuário logado
        else:
            usuario = Usuarios.objects.get(user_id = user_logado) # Buscando usuário administrador com base no usuário logado
            usuario = usuario.id # Obitendo o id  do usuário administrador

        venda = Venda.objects.get(id=venda)
        usuario_adm = venda.usuarios.id
        if usuario_adm == usuario: # Verificar autenticidade do usuário
            return render(
                request, 'delete-pedido-confirm.html', {'venda': venda})
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    def post(self, request, venda):
        user = request.user.has_perm('fluxo_de_caixa.delete_venda')
        if user == False:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

        user_logado = request.user # Obitendo o usuário logado
        user_logado = user_logado.id # obitendo o ID do usuário logado
        if Funcionario.objects.filter(user_id = user_logado): # verificando se o usuário existe em funcionários
            funcionario= Funcionario.objects.get(user__id = user_logado) # buscado funcionário baseado no usuário logado
            usuario= funcionario.usuarios.id # Buscando o ID dousuário administrador com base no usuário logado
        else:
            usuario = Usuarios.objects.get(user_id = user_logado) # Buscando usuário administrador com base no usuário logado
            usuario = usuario.id # Obitendo o id  do usuário administrador

        venda = Venda.objects.get(id=venda)
        usuario_adm = venda.usuarios.id
        if usuario_adm == usuario:
            venda.delete()
            return redirect('lista-vendas')
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

class DeleteItemPedido(LoginRequiredMixin, View):
    def get(self, request, item):
        user = request.user.has_perm('fluxo_de_caixa.delete_itemdopedido')
        if user == False:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

        item_pedido = ItemDoPedido.objects.get(id=item)
        return render(
            request, 'delete-itempedido-confirm.html', {'item_pedido': item_pedido})

    def post(self, request, item):
        user = request.user.has_perm('fluxo_de_caixa.delete_itemdopedido')
        if user == False:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

        item_pedido = ItemDoPedido.objects.get(id=item)
        venda_id = item_pedido.venda.id
        item_pedido.delete()
        return redirect('edit-pedido', venda=venda_id)

class Caixas(LoginRequiredMixin, View):

    def get(self, request):
        user = request.user.has_perm('fluxo_de_caixa.view_caixa')
        if user == False:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

        user_logado = request.user # Obitendo o usuário logado
        user_logado = user_logado.id # obitendo o ID do usuário logado
        if Funcionario.objects.filter(user_id = user_logado): # verificando se o usuário existe em funcionários
            funcionario= Funcionario.objects.get(user__id = user_logado) # buscado funcionário baseado no usuário logado
            usuario= funcionario.usuarios.usuario_cliente # Buscando o ID dousuário administrador com base no usuário logado
        else:
            usuario = Usuarios.objects.get(user_id = user_logado) # Buscando usuário administrador com base no usuário logado
            usuario = usuario.usuario_cliente # Obitendo o id  do usuário administrador

        caixa = Caixa.objects.filter(usuarios__usuario_cliente= usuario)
        caixa_user_logado = Caixa.objects.filter(usuarios__usuario_cliente= usuario, funcionario__user = user_logado)
        funcionarios= Funcionario.objects.filter(usuarios__usuario_cliente= usuario)

        return render(
            request, 'caixa.html',{'caixa':caixa,
                'funcionarios': funcionarios,
                'caixa_user_logado': caixa_user_logado
                })

    def post(self, request):
        user = request.user.has_perm('fluxo_de_caixa.view_caixa')
        if user == False:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

        data = {}
        data['nome_do_caixa'] = request.POST['nome_do_caixa']
        data['funcionario'] = request.POST['funcionario']

        user_logado = request.user # Obitendo o usuário logado
        user_logado = user_logado.id # obitendo o ID do usuário logado
        if Funcionario.objects.filter(user_id = user_logado): # verificando se o usuário existe em funcionários
            funcionario= Funcionario.objects.get(user__id = user_logado) # buscado funcionário baseado no usuário logado
            usuarioId= funcionario.usuarios.id # Buscando o ID dousuário administrador com base no usuário logado
            usuarioCliente= funcionario.usuarios.usuario_cliente # Buscando o ID dousuário administrador com base no usuário logado
        else:
            usuario = Usuarios.objects.get(user_id = user_logado) # Buscando usuário administrador com base no usuário logado
            usuarioId = usuario.id # Obitendo o id  do usuário administrador
            usuarioCliente= usuario.usuario_cliente # Obitendo o id  do usuário_cliente administrador

        novo_caixa = Caixa.objects.create(
            nome_do_caixa=request.POST['nome_do_caixa'],
            funcionario_id= request.POST['funcionario'],
            user = user_logado, usuarios_id = usuarioId,

            )
        data['novo_caixa'] = novo_caixa
        data['caixa'] = Caixa.objects.filter(usuarios__usuario_cliente= usuarioCliente)
        data['caixa_user_logado']= Caixa.objects.filter(usuarios__usuario_cliente= usuario, funcionario__user__id = user_logado)
        data['funcionarios']= Funcionario.objects.filter(usuarios__usuario_cliente= usuario)
        return render(
            request, 'caixa.html',data)

class CaixasUpdate(LoginRequiredMixin, View):
    
    def get(self, request, id):
        data={}
        user = request.user.has_perm('fluxo_de_caixa.view_caixa')
        if user == False:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

        user_logado = request.user # Obitendo o usuário logado
        user_logado = user_logado.id # obitendo o ID do usuário logado
        if Funcionario.objects.filter(user_id = user_logado): # verificando se o usuário existe em funcionários
            funcionario= Funcionario.objects.get(user__id = user_logado) # buscado funcionário baseado no usuário logado
            usuario= funcionario.usuarios.usuario_cliente # Buscando o ID dousuário administrador com base no usuário logado
        else:
            usuario = Usuarios.objects.get(user_id = user_logado) # Buscando usuário administrador com base no usuário logado
            usuario = usuario.usuario_cliente # Obitendo o id  do usuário administrador
        
        caixa = Caixa.objects.get(id=id)
        usuario_adm = caixa.usuarios.usuario_cliente
        if usuario_adm == usuario: # Verificar autenticidade do usuário
        
            data['caixa'] = Caixa.objects.get(id=id)
            data['funcionarios']= Funcionario.objects.filter(usuarios__usuario_cliente= usuario)
            return render( request, 'caixa-update.html', data)
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    def post(self, request, id):
        user = request.user.has_perm('fluxo_de_caixa.view_caixa')
        if user == False:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

        user_logado = request.user # Obitendo o usuário logado
        user_logado = user_logado.id # obitendo o ID do usuário logado
        if Funcionario.objects.filter(user_id = user_logado): # verificando se o usuário existe em funcionários
            funcionario= Funcionario.objects.get(user__id = user_logado) # buscado funcionário baseado no usuário logado
            usuarioId= funcionario.usuarios.id # Buscando o ID dousuário administrador com base no usuário logado
            
        else:
            usuario = Usuarios.objects.get(user_id = user_logado) # Buscando usuário administrador com base no usuário logado
            usuarioId = usuario.id # Obitendo o id  do usuário administrador
           
        caixa = Caixa.objects.get(id=id)
        usuario_adm = caixa.usuarios.id
        if usuario_adm == usuarioId: # Verificar autenticidade do usuário
            caixa.nome_do_caixa=request.POST['nome_do_caixa']
            caixa.funcionario_id= request.POST['funcionario']
            caixa.user = user_logado
            caixa.usuarios_id = usuarioId
            caixa.save()
            return redirect( 'caixa')
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
@login_required()
def caixa_delete(request, id):
    user = request.user.has_perm('pessoa.delete_fornecedor')
    if user == False:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    user_logado = request.user # Obitendo o usuário logado
    user_logado = user_logado.id # obitendo o ID do usuário logado
    if Funcionario.objects.filter(user_id = user_logado): # verificando se o usuário existe em funcionários
        funcionario= Funcionario.objects.get(user__id = user_logado) # buscado funcionário baseado no usuário logado
        usuarioId= funcionario.usuarios.id # Buscando o ID dousuário administrador com base no usuário logado
        
    else:
        usuario = Usuarios.objects.get(user_id = user_logado) # Buscando usuário administrador com base no usuário logado
        usuarioId = usuario.id # Obitendo o id  do usuário administrador
       
    caixa = Caixa.objects.get(id=id)
    usuario_adm = caixa.usuarios.id
    if usuario_adm == usuarioId: # Verificar autenticidade do usuário
        data  = {}
        if request.method == 'POST':
            caixa.delete()
            return redirect('caixa')
        else:
            return render(request, 'delete-caixa.html',data)
    else:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))


class CaixaDepositar(LoginRequiredMixin, View):

    def get(self, request, id):
        user = request.user.has_perm('fluxo_de_caixa.add_depositar_sacar')
        if user == False:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        
        user_logado = request.user # Obitendo o usuário logado
        user_logado = user_logado.id # obitendo o ID do usuário logado
        if Funcionario.objects.filter(user_id = user_logado): # verificando se o usuário existe em funcionários
            funcionario= Funcionario.objects.get(user__id = user_logado) # buscado funcionário baseado no usuário logado
            usuario= funcionario.usuarios.id # Buscando o ID dousuário administrador com base no usuário logado
        else:
            usuario = Usuarios.objects.get(user_id = user_logado) # Buscando usuário administrador com base no usuário logado
            usuario = usuario.id # Obitendo o id  do usuário administrador
        
        caixa = Caixa.objects.get(id=id)
        usuario_adm = caixa.usuarios.id
        if usuario_adm == usuario: # Verificar autenticidade do usuário

            today = date.today()

            depositos = Depositar_sacar.objects.filter(
                caixa__id = id, data_hora__contains= today).order_by('-id').order_by('-data_hora')

            caixa = Caixa.objects.get(id=id)

            DIA = request.GET.get('dia',None)
            DIA2 = request.GET.get('dia2',None)

            if DIA and DIA2 :
                depositos = Depositar_sacar.objects.filter(
                    data_hora__range= (DIA, DIA2), caixa__id = id).order_by('-data_hora')
            return render(
                request,'caixa-deposito.html',{'depositos':depositos,'caixa':caixa })
        else:
             return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    def post(self, request, id):
        user = request.user.has_perm('fluxo_de_caixa.add_depositar_sacar')
        if user == False:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

        today = date.today()
        #today = date.today()
        data = {}

        user_logado = request.user # Obitendo o usuário logado
        user_logado = user_logado.id # obitendo o ID do usuário logado
        if Funcionario.objects.filter(user_id = user_logado): # verificando se o usuário existe em funcionários
            funcionario= Funcionario.objects.get(user__id = user_logado) # buscado funcionário baseado no usuário logado
            usuario= funcionario.usuarios.id # Buscando o ID dousuário administrador com base no usuário logado
        else:
            usuario = Usuarios.objects.get(user_id = user_logado) # Buscando usuário administrador com base no usuário logado
            usuario = usuario.id # Obitendo o id  do usuário administrador
        
        caixa = Caixa.objects.get(id=id)
        usuario_adm = caixa.usuarios.id
        if usuario_adm == usuario: # Verificar autenticidade do usuário

            deposito = Depositar_sacar.objects.create(
                descricao=request.POST['descricao'],
                depositar=request.POST['depositar'].replace('.','').replace(',','.').replace('R$\xa0','').replace('R$',''),
                caixa_id = id, user = user_logado, usuarios_id = usuario,
                )
            data['deposito'] = deposito
            data['depositos'] = Depositar_sacar.objects.filter(caixa__id = id, data_hora__contains= today).order_by('-id')
            data['caixa'] = Caixa.objects.get(id=id)
            return render(
                request, 'caixa-deposito.html', data)
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

class CaixaSacar(LoginRequiredMixin, View):

    def get(self, request, id):
        user = request.user.has_perm('fluxo_de_caixa.add_depositar_sacar')
        if user == False:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

        user_logado = request.user # Obitendo o usuário logado
        user_logado = user_logado.id # obitendo o ID do usuário logado
        if Funcionario.objects.filter(user_id = user_logado): # verificando se o usuário existe em funcionários
            funcionario= Funcionario.objects.get(user__id = user_logado) # buscado funcionário baseado no usuário logado
            usuario= funcionario.usuarios.id # Buscando o ID dousuário administrador com base no usuário logado
        else:
            usuario = Usuarios.objects.get(user_id = user_logado) # Buscando usuário administrador com base no usuário logado
            usuario = usuario.id # Obitendo o id  do usuário administrador

        caixa = Caixa.objects.get(id=id)
        usuario_adm = caixa.usuarios.id
        if usuario_adm == usuario: # Verificar autenticidade do usuário
            
            today = date.today()
            sacar = Depositar_sacar.objects.filter(
                caixa__id = id, data_hora__contains= today).order_by('-id').order_by('-data_hora')

            DIA = request.GET.get('dia',None)
            DIA2 = request.GET.get('dia2',None)

            if DIA and DIA2 :
                sacar = Depositar_sacar.objects.filter(
                    data_hora__range= (DIA, DIA2), caixa__id = id).order_by('-data_hora')
            return render(
                request, 'caixa-sacar.html',{'sacar':sacar, 'caixa':caixa})
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    def post(self, request, id):
        user = request.user.has_perm('fluxo_de_caixa.add_depositar_sacar')
        if user == False:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

        today = date.today()

        data = {}

        user_logado = request.user # Obitendo o usuário logado
        user_logado = user_logado.id # obitendo o ID do usuário logado
        if Funcionario.objects.filter(user_id = user_logado): # verificando se o usuário existe em funcionários
            funcionario= Funcionario.objects.get(user__id = user_logado) # buscado funcionário baseado no usuário logado
            usuario= funcionario.usuarios.id # Buscando o ID dousuário administrador com base no usuário logado
        else:
            usuario = Usuarios.objects.get(user_id = user_logado) # Buscando usuário administrador com base no usuário logado
            usuario = usuario.id # Obitendo o id  do usuário administrador

        caixa = Caixa.objects.get(id=id)
        usuario_adm = caixa.usuarios.id
        if usuario_adm == usuario: # Verificar autenticidade do usuário

            deposito = Depositar_sacar.objects.create(
                descricao= request.POST['descricao'],
                sacar= request.POST['sacar'].replace('.','').replace(',','.').replace('R$\xa0','').replace('R$',''),
                caixa_id= id, user = user_logado, usuarios_id = usuario,
                )
            data['deposito'] = deposito
            data['sacar'] = Depositar_sacar.objects.filter(
                caixa__id = id, data_hora__contains= today).order_by('-id')
            data['caixa'] = Caixa.objects.get(id=id)
            return render(
                request, 'caixa-sacar.html', data)
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

class AbrirFeixarCaixa(LoginRequiredMixin, View):

    def get(self, request, id):
        user = request.user.has_perm('fluxo_de_caixa.add_depositar_sacar')
        if user == False:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

        today = date.today()
        user_logado = request.user # Obitendo o usuário logado
        user_logado = user_logado.id # obitendo o ID do usuário logado
        if Funcionario.objects.filter(user_id = user_logado): # verificando se o usuário existe em funcionários
            funcionario= Funcionario.objects.get(user__id = user_logado) # buscado funcionário baseado no usuário logado
            usuario= funcionario.usuarios.id # Buscando o ID dousuário administrador com base no usuário logado
        else:
            usuario = Usuarios.objects.get(user_id = user_logado) # Buscando usuário administrador com base no usuário logado
            usuario = usuario.id # Obitendo o id  do usuário administrador

        historico_do_caixa = Caixa.objects.get(id=id)
        usuario_adm = historico_do_caixa.usuarios.id
        if usuario_adm == usuario: # Verificar autenticidade do usuário

            historico_do_caixa = Depositar_sacar.objects.filter(
                Q(estadoDoCaixa='Feixado') | Q(estadoDoCaixa='Aberto'), caixa__id = id, user = user_logado,data_hora__contains= today).order_by('-id')

            estado_do_caixa= Depositar_sacar.objects.filter(caixa__id = id).last()

            DIA = request.GET.get('dia',None)
            DIA2 = request.GET.get('dia2',None)

            if DIA and DIA2 :
                historico_do_caixa = Depositar_sacar.objects.filter(
                Q(estadoDoCaixa='Feixado') | Q(estadoDoCaixa='Aberto'), data_hora__range= (DIA, DIA2), caixa__id = id, user = user_logado, data_hora__contains= today).order_by('-id')
            return render(
                request, 'abrir-feixar-caixa.html',{
                    'historico_do_caixa':historico_do_caixa,
                    'estado_do_caixa': estado_do_caixa}
                )
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    def post(self, request, id):
        user = request.user.has_perm('fluxo_de_caixa.add_depositar_sacar')
        if user == False:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

        today = date.today()

        data = {}

        data['descricao'] = request.POST['descricao']
        data['estadoDoCaixa'] = request.POST['estadoDoCaixa']

        user_logado = request.user # Obitendo o usuário logado
        user_logado = user_logado.id # obitendo o ID do usuário logado
        if Funcionario.objects.filter(user_id = user_logado): # verificando se o usuário existe em funcionários
            funcionario= Funcionario.objects.get(user__id = user_logado) # buscado funcionário baseado no usuário logado
            usuario= funcionario.usuarios.id # Buscando o ID dousuário administrador com base no usuário logado
        else:
            usuario = Usuarios.objects.get(user_id = user_logado) # Buscando usuário administrador com base no usuário logado
            usuario = usuario.id # Obitendo o id  do usuário administrador

        historico_do_caixa = Caixa.objects.get(id=id)
        usuario_adm = historico_do_caixa.usuarios.id
        if usuario_adm == usuario: # Verificar autenticidade do usuário

            venda_sedula= Venda.objects.filter(
                data_hora__contains= today, user_2 = user_logado, usuarios_id = usuario).aggregate(total_venda_cedula=Sum('valor_cedula'))
            venda_sedula = venda_sedula['total_venda_cedula']or 0

            estado_do_caixa= Depositar_sacar.objects.filter(caixa__id = id).aggregate(vendas=Sum('venda_realizadas'))
            estado_do_caixa= estado_do_caixa['vendas'] or None

            if estado_do_caixa != None:
                ultimas_vendas= estado_do_caixa
            else:
                ultimas_vendas = 0
            ultimas_vendas= float(venda_sedula) - float(ultimas_vendas)

            saldoEmCaixa= Caixa.objects.get(id = id) # buscando o saldo atual do caiza
            saldoEmCaixa= saldoEmCaixa.valor_atualizado
            saldoEmCaixa= float(saldoEmCaixa) + float(ultimas_vendas)

            deposito = Depositar_sacar.objects.create(
                descricao= request.POST['descricao'],
                estadoDoCaixa= request.POST['estadoDoCaixa'],
                caixa_id= id, user = user_logado, usuarios_id = usuario,
                venda_realizadas= ultimas_vendas, depositar= ultimas_vendas,
                saldo_em_caixa= saldoEmCaixa
                )
            data['deposito'] = deposito
            data['historico_do_caixa'] = Depositar_sacar.objects.filter(
                Q(estadoDoCaixa='Feixado') | Q(estadoDoCaixa='Aberto'), caixa__id = id, user = user_logado,data_hora__contains= today).order_by('-id')
            data['estado_do_caixa']= Depositar_sacar.objects.filter(caixa__id = id).last()

            return render(
                request, 'abrir-feixar-caixa.html', data)
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
