from datetime import date
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import View
from .models import Venda, Depositar_sacar, Caixa
from .models import Produto
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from pessoa.models import Funcionario
from django.db.models import Sum 
from django.db.models import Q
from pessoa.models import Cliente
from .models import ItemDoPedido
from usuarios.permitir_autorizar import autenticar_usuario, autorizarcao_de_reistro

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
        user_logado = request.user.id
        usuario_cliente = autenticar_usuario(user_logado)
        autorizarcao_de_reistros = autorizarcao_de_reistro(usuario_cliente)
        if autorizarcao_de_reistros:
            return autorizarcao_de_reistros

        data = {}
        if request.POST['venda_id']:
            vendas= Venda.objects.get(id= request.POST['venda_id'])
            usuario_adm = vendas.usuarios.id

            if usuario_adm == usuario_cliente:
                venda = Venda.objects.get(id = request.POST['venda_id'])
                venda.desconto = request.POST['desconto'].replace(',', '.').replace('%', '') or 0
                venda.tipo_de_pagamento_id = request.POST['pagamento']  or 1
                venda.finalizada = request.POST.get('finalizada', False)
                if request.POST['cliente']:
                    venda.cliente_id = request.POST['cliente']
                venda.valor_recebido = request.POST['valor_recebido'].replace('.','').replace(',','.').replace('R$\xa0','').replace('R$','')
                venda.valor_credito = request.POST['valor_credito'].replace('.','').replace(',','.').replace('R$\xa0','').replace('R$','')
                venda.valor_debito = request.POST['valor_debito'].replace('.','').replace(',','.').replace('R$\xa0','').replace('R$','')
                venda.user_2 = user_logado
                venda.venda_id = request.POST['venda_id']

                venda.save()
            
            else:
                return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        else:
            user = request.user.has_perm('fluxo_de_caixa.add_venda')
            if user == False:
                return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

            venda = Venda.objects.create(user = user_logado, usuarios_id = usuario_cliente)

        itens = venda.itemdopedido_set.all().order_by('-id')
        data['venda'] = venda
        data['itens'] = itens
        data['usuarios'] = usuario_cliente
        data['produto'] = Produto.objects.filter(usuarios_id = usuario_cliente)
        data['cliente'] = Cliente.objects.filter(usuarios_id = usuario_cliente)
        return render(
            request, 'novo-pedido.html', data)

class NovoPedido(LoginRequiredMixin, View):

    def post(self, request):
        user = request.user.has_perm('fluxo_de_caixa.add_venda')
        if user == False:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

        user_logado = request.user.id
        usuario_cliente = autenticar_usuario(user_logado)
        autorizarcao_de_reistros = autorizarcao_de_reistro(usuario_cliente)
        if autorizarcao_de_reistros:
            return autorizarcao_de_reistros
        data = {}
        data['venda_id'] = request.POST['venda_id']

        venda = Venda.objects.create(user = user_logado, usuarios_id = usuario_cliente)

        itens = venda.itemdopedido_set.all().order_by('-id')
        data['venda'] = venda
        data['itens'] = itens
        data['usuarios'] = usuario_cliente
        data['produto'] = Produto.objects.filter(usuarios_id = usuario_cliente)
        data['cliente'] = Cliente.objects.filter (usuarios_id = usuario_cliente)
        return render(
            request, 'novo-pedido.html', data)

class NovoItemPedido(LoginRequiredMixin, View):

    def get(self, request):
        user = request.user.has_perm('fluxo_de_caixa.add_venda')
        if user == False:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    def post(self, request, venda):
        user = request.user.has_perm('fluxo_de_caixa.add_venda')
        if user == False:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        user_logado = request.user.id
        usuario_cliente = autenticar_usuario(user_logado)
        autorizarcao_de_reistros = autorizarcao_de_reistro(usuario_cliente)
        if autorizarcao_de_reistros:
            return autorizarcao_de_reistros

        data = {}
        produto= Produto.objects.filter(
            usuarios_id= usuario_cliente, codigo= request.POST['produto_codigo'] ) or 0
        if request.POST['produto_select']  and request.POST['produto_codigo'] :
            data={}
            data['mensagen_de_erro_campo_obrigatorio'] = 'Preencha apenas um dos campos a baixa'
            venda = Venda.objects.get(id=venda)
            data['venda'] = venda
            data['itens'] = venda.itemdopedido_set.all()
            data['produto'] = Produto.objects.filter(
                user = user_logado, usuarios_id = usuario_cliente)
            data['cliente'] = Cliente.objects.filter(
                user = user_logado, usuarios_id = usuario_cliente)
            return render(
                request, 'novo-pedido.html', data)
        
        if produto != 0:
            produto= produto.latest('pk').pk
        if request.POST['produto_codigo'] == '':
            produto = request.POST['produto_select']
            
        if request.POST['produto_select'] == '' and request.POST['produto_codigo'] == '':
            data={}
            data['mensagen_de_erro_campo_obrigatorio'] = 'Preencha um do campos a baixa'
            venda = Venda.objects.get(id=venda)
            data['venda'] = venda
            data['itens'] = venda.itemdopedido_set.all()
            data['produto'] = Produto.objects.filter(usuarios_id = usuario_cliente)
            data['cliente'] = Cliente.objects.filter(usuarios_id = usuario_cliente)
            return render(
                request, 'novo-pedido.html', data)
        elif produto == 0 :
            data['mensagen_de_erro'] = 'Produto não cadastrado!'
            data['mensagen_de_erro_dica'] = 'Verifica o cdigo e tente novamente!' 
            data['mensagen_de_erro_acao'] = 'Para feichar, pressione ( Alt + X ) !'
            venda = Venda.objects.get(id=venda)
            data['venda'] = venda
            data['itens'] = venda.itemdopedido_set.all()
            data['produto'] = Produto.objects.filter( usuarios_id = usuario_cliente)
            data['cliente'] = Cliente.objects.filter(usuarios_id = usuario_cliente)
            return render(
                request, 'novo-pedido.html', data)
        else:
            item = ItemDoPedido.objects.create(
                produto_id = produto,
                quantidade_de_itens=request.POST['quantidade'].replace(',', '.') or 0,
                desconto=request.POST['desconto'].replace(',', '.') or 0,
                venda_id=venda, user = user_logado, usuarios_id = usuario_cliente)

            data['venda'] = item.venda
            data['itens'] = item.venda.itemdopedido_set.all().order_by('-id')
            data['usuarios'] = usuario_cliente
            data['produto'] = Produto.objects.filter(usuarios_id = usuario_cliente)
            data['cliente'] = Cliente.objects.filter(usuarios_id = usuario_cliente)
            return render(
                request, 'novo-pedido.html', data)

class SaidaDeMercadoria(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user.has_perm('fluxo_de_caixa.add_venda')
        if user == False:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        user_logado = request.user.id
        usuario_cliente = autenticar_usuario(user_logado)
        autorizarcao_de_reistros = autorizarcao_de_reistro(usuario_cliente)
        if autorizarcao_de_reistros:
            return autorizarcao_de_reistros

        data = {}
        data['produto'] = Produto.objects.filter(usuarios_id = usuario_cliente)
        return render(
            request, 'saida_mercadoria.html', data)

    def post(self, request):
        user = request.user.has_perm('fluxo_de_caixa.add_venda')
        if user == False:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        user_logado = request.user.id
        usuario_cliente = autenticar_usuario(user_logado)
        autorizarcao_de_reistros = autorizarcao_de_reistro(usuario_cliente)
        if autorizarcao_de_reistros:
            return autorizarcao_de_reistros

        data = {}
        produto= Produto.objects.filter(
            usuarios_id= usuario_cliente, codigo= request.POST['produto_codigo'] ) or 0
        
        if request.POST['produto_select']  and request.POST['produto_codigo'] :
            data={}
            data['mensagen_de_erro_campo_obrigatorio'] = 'Preencha apenas um dos campos a baixa'
            data['produto'] = Produto.objects.filter(
                    user = user_logado, usuarios_id = usuario_cliente)
            return render(
                request, 'saida_mercadoria.html', data)
        
        if produto != 0:
            produto= produto.latest('pk').pk
        if request.POST['produto_codigo'] == '':
            produto = request.POST['produto_select']
            
        if request.POST['produto_select'] == '' and request.POST['produto_codigo'] == '':
            data={}
            data['mensagen_de_erro_campo_obrigatorio'] = 'Preencha um do campos a baixa'
            data['produto'] = Produto.objects.filter(
                    user = user_logado, usuarios_id = usuario_cliente)
            return render(
                request, 'saida_mercadoria.html', data)
        elif produto == 0 :
            data['mensagen_de_erro'] = 'Produto não cadastrado!'
            data['mensagen_de_erro_dica'] = 'Verifica o cdigo e tente novamente!' 
            data['mensagen_de_erro_acao'] = 'Para feichar, pressione ( Alt + X ) !'
            data['produto'] = Produto.objects.filter(
                    user = user_logado, usuarios_id = usuario_cliente)
            return render(
                request, 'saida_mercadoria.html', data)
        else:
            produtoestoque= Produto.objects.get(id = produto)
            produto_estoque =  produtoestoque.estoque
            if float(produto_estoque) < float(request.POST['estoque_fisico_atual']):
                data['mensagen_de_erro_2'] = 'Estoque menor que a quantidade inserida!'
                data['mensagen_de_erro_dica'] = 'Seu estoque deve está desatualizado, atualize-o e tente novamente!' 
                data['mensagen_de_erro_acao'] = 'Para feichar, pressione ( Alt + X ) !'
                data['produto'] = Produto.objects.filter(
                    user = user_logado, usuarios_id = usuario_cliente)
                return render(
                request, 'saida_mercadoria.html', data)
            else:
                venda = Venda.objects.create(user = user_logado, usuarios_id = usuario_cliente)
                item = ItemDoPedido.objects.create(
                    produto_id = produto,
                    estoque_fisico_atual=request.POST['estoque_fisico_atual'],
                    venda_id=venda.id, user = user_logado, usuarios_id = usuario_cliente)
                    
                data['saida'] = ItemDoPedido.objects.get(id=item.id)
                data['produto'] = Produto.objects.filter(usuarios_id = usuario_cliente)
                return render(
                    request, 'saida_mercadoria.html', data)

class ListaVendas(LoginRequiredMixin, View):
    def get(self, request):
        data = {}

        user = request.user.has_perm('fluxo_de_caixa.view_venda')
        if user == False:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        user_logado = request.user.id
        usuario_cliente = autenticar_usuario(user_logado)
        autorizarcao_de_reistros = autorizarcao_de_reistro(usuario_cliente)
        if autorizarcao_de_reistros:
            return autorizarcao_de_reistros

        today = date.today()
        cliente=request.GET.get('cliente', None)
        mes= request.GET.get('mes',None)
        id_venda= request.GET.get('id_venda',None)
        dia= request.GET.get('dia',None)

        vendas = Venda.objects.filter(
            data_hora__gte=today, usuarios_id= usuario_cliente).order_by('-id') 
        if dia:
            vendas = Venda.objects.filter(
                data_hora__contains=dia, usuarios_id= usuario_cliente).order_by('-id')
        if mes:
            vendas = Venda.objects.filter(
                data_hora__contains=mes, usuarios_id= usuario_cliente).order_by('-id')
        if id_venda:
            vendas = Venda.objects.filter( usuarios_id= usuario_cliente, id__icontains=id_venda)
        if cliente:
            vendas = Venda.objects.filter( usuarios_id= usuario_cliente, cliente_id=cliente)
        data['vendas'] = vendas
        data['cliente'] = Cliente.objects.filter(usuarios_id= usuario_cliente)
        return render(request, 'lista-vendas.html', data)


class ListaVendaPorUsuario(LoginRequiredMixin, View):
    def get(self, request):
        data = {}

        user = request.user.has_perm('fluxo_de_caixa.view_venda')
        if user == False:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        user_logado = request.user.id
        usuario_cliente = autenticar_usuario(user_logado)
        autorizarcao_de_reistros = autorizarcao_de_reistro(usuario_cliente)
        if autorizarcao_de_reistros:
            return autorizarcao_de_reistros

        today = date.today()
        Mes= request.GET.get('mes',None)
        busca= request.GET.get('venda',None)
        Dia= request.GET.get('dia',None)

        vendas = Venda.objects.filter(
            data_hora__gte=today, user = user_logado, usuarios_id= usuario_cliente).order_by('-id') #__startswith, __contains
        total_vendas= vendas.aggregate(total=Sum("valor_com_desconto"))
        total_desconto= vendas.aggregate(total=Sum("total_desconto"))
        if Dia:
            vendas = Venda.objects.filter(
                data_hora__contains=Dia, user = user_logado, usuarios_id= usuario_cliente).order_by('-id')#data_hora__day= Dia
            total_vendas= vendas.aggregate(total=Sum("valor_com_desconto"))
            total_desconto= vendas.aggregate(total=Sum("total_desconto"))
        if Mes:
            vendas = Venda.objects.filter(
                data_hora__year__contains=today.year, data_hora__month__contains=Mes, user = user_logado, usuarios_id= usuario_cliente ).order_by('-id')
            total_vendas= vendas.aggregate(total=Sum("valor_com_desconto"))
            total_desconto= vendas.aggregate(total=Sum("total_desconto"))

        if busca:
            vendas = Venda.objects.filter(
                user = user_logado, usuarios_id= usuario_cliente, id__icontains=busca)
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
        user_logado = request.user.id
        usuario_cliente = autenticar_usuario(user_logado)
        autorizarcao_de_reistros = autorizarcao_de_reistro(usuario_cliente)
        if autorizarcao_de_reistros:
            return autorizarcao_de_reistros

        today = date.today()
        Mes= request.GET.get('mes',None)
        busca= request.GET.get('venda',None)
        Dia= request.GET.get('dia',None)

        vendas = Venda.objects.filter(
            data_hora__gte=today, user_2 = user_logado, usuarios_id= usuario_cliente).order_by('-id') #__startswith, __contains
        total_vendas= vendas.aggregate(total=Sum("valor_com_desconto"))

        if Dia:
            vendas = Venda.objects.filter(
                data_hora__contains=Dia, user_2 = user_logado, usuarios_id= usuario_cliente).order_by('-id')#data_hora__day= Dia
            total_vendas= vendas.aggregate(total=Sum("valor_com_desconto"))

        if Mes:
            vendas = Venda.objects.filter(
                data_hora__year__contains=today.year, data_hora__month__contains=Mes, user_2 = user_logado, usuarios_id= usuario_cliente ).order_by('-id')
            total_vendas= vendas.aggregate(total=Sum("valor_com_desconto"))

        if busca:
            vendas = Venda.objects.filter(
                user_2 = user_logado, usuarios_id= usuario_cliente, id__icontains=busca)
            total_vendas= vendas.aggregate(total=Sum("valor_com_desconto"))
            
        data['vendas'] = vendas
        data['total_vendas']= total_vendas
        return render(request, 'vendas-pagas.html', data)

class EditPedido(LoginRequiredMixin, View):
    def get(self, request, venda):
        user = request.user.has_perm('fluxo_de_caixa.view_venda')
        if user == False:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        user_logado = request.user.id
        usuario_cliente = autenticar_usuario(user_logado)
        autorizarcao_de_reistros = autorizarcao_de_reistro(usuario_cliente)
        if autorizarcao_de_reistros:
            return autorizarcao_de_reistros

        data = {}
        venda = Venda.objects.get(id=venda)
        usuario_adm = venda.usuarios.id
        if usuario_adm == usuario_cliente:
            data['venda'] = venda
            data['itens'] = venda.itemdopedido_set.all()
            data['usuarios'] = usuario_cliente
            data['produto'] = Produto.objects.filter(usuarios_id = usuario_cliente)
            data['cliente'] = Cliente.objects.filter(usuarios_id = usuario_cliente)
            return render(
                request, 'novo-pedido.html', data)
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        
class DeletePedido(LoginRequiredMixin, View):
    def get(self, request, venda):
        user = request.user.has_perm('fluxo_de_caixa.delete_venda')
        if user == False:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        user_logado = request.user.id
        usuario_cliente = autenticar_usuario(user_logado)
        autorizarcao_de_reistros = autorizarcao_de_reistro(usuario_cliente)
        if autorizarcao_de_reistros:
            return autorizarcao_de_reistros

        venda = Venda.objects.get(id=venda)
        usuario_adm = venda.usuarios.id
        if usuario_adm == usuario_cliente: 
            return render(
                request, 'delete-pedido-confirm.html', {'venda': venda})
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    def post(self, request, venda):
        user = request.user.has_perm('fluxo_de_caixa.delete_venda')
        if user == False:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        user_logado = request.user.id
        usuario_cliente = autenticar_usuario(user_logado)
        autorizarcao_de_reistros = autorizarcao_de_reistro(usuario_cliente)
        if autorizarcao_de_reistros:
            return autorizarcao_de_reistros

        venda = Venda.objects.get(id=venda)
        usuario_adm = venda.usuarios.id
        if usuario_adm == usuario_cliente:
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
        user_logado = request.user.id
        usuario_cliente = autenticar_usuario(user_logado)
        autorizarcao_de_reistros = autorizarcao_de_reistro(usuario_cliente)
        if autorizarcao_de_reistros:
            return autorizarcao_de_reistros
        data = {}
        data['caixa'] = Caixa.objects.filter(usuarios_id= usuario_cliente)
        data['caixa_user_logado'] = Caixa.objects.filter(usuarios_id= usuario_cliente, funcionario__user = user_logado)
        data['funcionarios']= Funcionario.objects.filter(usuarios_id= usuario_cliente)
        return render(
            request, 'caixa.html',data)

    def post(self, request):
        user = request.user.has_perm('fluxo_de_caixa.view_caixa')
        if user == False:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        user_logado = request.user.id
        usuario_cliente = autenticar_usuario(user_logado)
        autorizarcao_de_reistros = autorizarcao_de_reistro(usuario_cliente)
        if autorizarcao_de_reistros:
            return autorizarcao_de_reistros

        data = {}
        novo_caixa = Caixa.objects.create(
            nome_do_caixa=request.POST['nome_do_caixa'],
            funcionario_id= request.POST['funcionario'],
            user = user_logado, usuarios_id = usuario_cliente,
            )
        data['novo_caixa'] = novo_caixa
        data['caixa'] = Caixa.objects.filter(usuarios_id= usuario_cliente)
        data['caixa_user_logado']= Caixa.objects.filter(usuarios_id= usuario_cliente, funcionario__user__id = user_logado)
        data['funcionarios']= Funcionario.objects.filter(usuarios_id= usuario_cliente)
        return render(
            request, 'caixa.html',data)

class CaixasUpdate(LoginRequiredMixin, View):
    
    def get(self, request, id):
        data={}
        user = request.user.has_perm('fluxo_de_caixa.view_caixa')
        if user == False:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        user_logado = request.user.id
        usuario_cliente = autenticar_usuario(user_logado)
        autorizarcao_de_reistros = autorizarcao_de_reistro(usuario_cliente)
        if autorizarcao_de_reistros:
            return autorizarcao_de_reistros
        
        caixa = Caixa.objects.get(id=id)
        usuario_adm = caixa.usuarios.id
        if usuario_adm == usuario_cliente:
        
            data['caixa'] = Caixa
            data['funcionarios']= Funcionario.objects.filter(usuarios_id = usuario_cliente)
            return render( request, 'caixa-update.html', data)
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    def post(self, request, id):
        user = request.user.has_perm('fluxo_de_caixa.view_caixa')
        if user == False:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        user_logado = request.user.id
        usuario_cliente = autenticar_usuario(user_logado)
        autorizarcao_de_reistros = autorizarcao_de_reistro(usuario_cliente)
        if autorizarcao_de_reistros:
            return autorizarcao_de_reistros
           
        caixa = Caixa.objects.get(id=id)
        usuario_adm = caixa.usuarios.id
        if usuario_adm == usuario_cliente:
            caixa.nome_do_caixa=request.POST['nome_do_caixa']
            caixa.funcionario_id= request.POST['funcionario']
            caixa.user = user_logado
            caixa.usuarios_id = usuario_cliente
            caixa.save()
            return redirect( 'caixa')
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
@login_required()
def caixa_delete(request, id):
    user = request.user.has_perm('pessoa.delete_fornecedor')
    if user == False:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    user_logado = request.user.id
    usuario_cliente = autenticar_usuario(user_logado)
    autorizarcao_de_reistros = autorizarcao_de_reistro(usuario_cliente)
    if autorizarcao_de_reistros:
        return autorizarcao_de_reistros
       
    caixa = Caixa.objects.get(id=id)
    usuario_adm = caixa.usuarios.id
    if usuario_adm == usuario_cliente: 
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
        user_logado = request.user.id
        usuario_cliente = autenticar_usuario(user_logado)
        autorizarcao_de_reistros = autorizarcao_de_reistro(usuario_cliente)
        if autorizarcao_de_reistros:
            return autorizarcao_de_reistros
        
        caixa = Caixa.objects.get(id=id)
        usuario_adm = caixa.usuarios.id
        if usuario_adm == usuario_cliente:
            today = date.today()
            depositos = Depositar_sacar.objects.filter(
                caixa__id = id, data_hora__contains= today).order_by('-id').order_by('-data_hora')
            caixa = Caixa.objects.get(id=id)
            dia = request.GET.get('dia',None)
            dia2 = request.GET.get('dia2',None)
            if dia and dia2 :
                depositos = Depositar_sacar.objects.filter(
                    data_hora__range= (dia, dia2), caixa__id = id).order_by('-data_hora')
            return render(
                request,'caixa-deposito.html',{'depositos':depositos,'caixa':caixa })
        else:
             return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    def post(self, request, id):
        user = request.user.has_perm('fluxo_de_caixa.add_depositar_sacar')
        if user == False:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        user_logado = request.user.id
        usuario_cliente = autenticar_usuario(user_logado)
        autorizarcao_de_reistros = autorizarcao_de_reistro(usuario_cliente)
        if autorizarcao_de_reistros:
            return autorizarcao_de_reistros

        today = date.today()
        data = {} 
        caixa = Caixa.objects.get(id=id)
        usuario_adm = caixa.usuarios.id
        caixa = Depositar_sacar.objects.filter(caixa__id = id).last()
        if usuario_adm == usuario_cliente:

            deposito = Depositar_sacar.objects.create(
                descricao=request.POST['descricao'],
                depositar=request.POST['depositar'].replace('.','').replace(',','.').replace('R$\xa0','').replace('R$',''),
                caixa_id = id, user = user_logado, usuarios_id = usuario_cliente,
                estado_do_caixa = caixa.estado_do_caixa
                )
            data['deposito'] = deposito
            data['depositos'] = Depositar_sacar.objects.filter(
                caixa__id = id, data_hora__contains= today).order_by('-id')
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

        user_logado = request.user.id
        usuario_cliente = autenticar_usuario(user_logado)
        autorizarcao_de_reistros = autorizarcao_de_reistro(usuario_cliente)
        if autorizarcao_de_reistros:
            return autorizarcao_de_reistros

        caixa = Caixa.objects.get(id=id)
        usuario_adm = caixa.usuarios.id
        if usuario_adm == usuario_cliente:
            today = date.today()
            sacar = Depositar_sacar.objects.filter(
                caixa__id = id, data_hora__contains= today).order_by('-id').order_by('-data_hora')
            dia = request.GET.get('dia',None)
            dia2 = request.GET.get('dia2',None)
            if dia and dia2 :
                sacar = Depositar_sacar.objects.filter(
                    data_hora__range= (dia, dia2), caixa__id = id).order_by('-data_hora')
            return render(
                request, 'caixa-sacar.html',{'sacar':sacar, 'caixa':caixa})
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    def post(self, request, id):
        user = request.user.has_perm('fluxo_de_caixa.add_depositar_sacar')
        if user == False:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        user_logado = request.user.id
        usuario_cliente = autenticar_usuario(user_logado)
        autorizarcao_de_reistros = autorizarcao_de_reistro(usuario_cliente)
        if autorizarcao_de_reistros:
            return autorizarcao_de_reistros

        today = date.today()
        data = {}
        caixa = Caixa.objects.get(id=id)
        usuario_adm = caixa.usuarios.id
        caixa = Depositar_sacar.objects.filter(caixa__id = id).last()
        if usuario_adm == usuario_cliente: 
            deposito = Depositar_sacar.objects.create(
                descricao= request.POST['descricao'],
                sacar= request.POST['sacar'].replace('.','').replace(',','.').replace('R$\xa0','').replace('R$',''),
                caixa_id= id, user = user_logado, usuarios_id = usuario_cliente,
                estado_do_caixa = caixa.estado_do_caixa
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
        user_logado = request.user.id
        usuario_cliente = autenticar_usuario(user_logado)
        autorizarcao_de_reistros = autorizarcao_de_reistro(usuario_cliente)
        if autorizarcao_de_reistros:
            return autorizarcao_de_reistros

        today = date.today()
        caixa = Caixa.objects.get(id=id)
        usuario_adm = caixa.usuarios.id
        if usuario_adm == usuario_cliente: 

            historico_do_caixa = Depositar_sacar.objects.filter(
                Q(estado_do_caixa='Feixado') | Q(estado_do_caixa='Aberto'), caixa__id = id, user = user_logado,data_hora__contains= today).order_by('-id')
            estado_do_caixa= Depositar_sacar.objects.filter(caixa__id = id).last()
            dia = request.GET.get('dia',None)
            dia2 = request.GET.get('dia2',None)

            if dia and dia2 :
                historico_do_caixa = Depositar_sacar.objects.filter(
                Q(estado_do_caixa='Feixado') | Q(estado_do_caixa='Aberto'), data_hora__range= (dia, dia2), caixa__id = id, user = user_logado, data_hora__contains= today).order_by('-id')
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
        user_logado = request.user.id
        usuario_cliente = autenticar_usuario(user_logado)
        autorizarcao_de_reistros = autorizarcao_de_reistro(usuario_cliente)
        if autorizarcao_de_reistros:
            return autorizarcao_de_reistros

        today = date.today()
        data = {}
        data['descricao'] = request.POST['descricao']
        data['estado_do_caixa'] = request.POST['estado_do_caixa']
        historico_do_caixa = Caixa.objects.get(id=id)
        usuario_adm = historico_do_caixa.usuarios.id
        if usuario_adm == usuario_cliente: 

            venda_sedula= Venda.objects.filter(
                data_hora__contains= today, user_2 = user_logado, usuarios_id = usuario_cliente).aggregate(total_venda_cedula=Sum('valor_cedula'))
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
                estado_do_caixa= request.POST['estado_do_caixa'],
                caixa_id= id, user = user_logado, usuarios_id = usuario_cliente,
                venda_realizadas= ultimas_vendas, depositar= ultimas_vendas,
                saldo_em_caixa= saldoEmCaixa,
                )
            data['deposito'] = deposito
            data['historico_do_caixa'] = Depositar_sacar.objects.filter(
                Q(estado_do_caixa='Feixado') | Q(estado_do_caixa='Aberto'), caixa__id = id, user = user_logado,data_hora__contains= today).order_by('-id')
            data['estado_do_caixa']= estado_do_caixa = Depositar_sacar.objects.filter(caixa__id = id).last()

            return render(
                request, 'abrir-feixar-caixa.html', data)
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
