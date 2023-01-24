import datetime
from django.shortcuts import render, redirect
from django.views import View
from fluxo_de_caixa.models import Depositar_sacar, Venda
from fluxo_de_caixa.models import ItemDoPedido
from django.db.models import Q
from .models import Contas, Pagamento, ParcelasConta
from .models import Gastos_extras
from .models import Tipo_de_conta
from .models import GastosExtrasCategoria
from pessoa.models import Cliente
from produto.models import EntradaMercadoria
from usuarios.models import Cobranca
from django.db.models import Sum, Count, F 
from datetime import date
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.conf import settings
from usuarios.permitir_autorizar import autenticar_usuario, autorizarcao_de_reistro, registro_de_dados

class GastosExtras(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user.has_perm('financeiro.add_gastos_extras')
        if user == False:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        user_logado = request.user.id
        usuario_cliente = autenticar_usuario(user_logado)
        autorizarcao_de_reistros = autorizarcao_de_reistro(usuario_cliente)
        if autorizarcao_de_reistros:
            return autorizarcao_de_reistros

        hoje = date.today()
        mes_atual = hoje.month
        ano = hoje.year
        data={} 
        data['gastos_extras'] = Gastos_extras.objects.filter(
            usuarios_id= usuario_cliente, data_hora__month = mes_atual, data_hora__year= ano ).order_by('-id')
        data['categoria_de_gastos']= GastosExtrasCategoria.objects.filter(
            usuarios_id= usuario_cliente).order_by('-id')
        data['hoje']= hoje
        return render(
            request, 'financeiro/gastos-extras.html', data)
       
    def post(self, request ):
        user = request.user.has_perm('financeiro.add_gastos_extras')
        if user == False:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        user_logado = request.user.id
        usuario_cliente = autenticar_usuario(user_logado)
        autorizarcao_de_reistros = autorizarcao_de_reistro(usuario_cliente)
        if autorizarcao_de_reistros:
            return autorizarcao_de_reistros 

        hoje = date.today()
        mes_atual = hoje.month
        ano = hoje.year
        data = {}
        gastos_extras = Gastos_extras.objects.create(
            descricao = request.POST['descricao'],
            gastosExtrasCategoria_id = request.POST['categoria'],
            valor = request.POST['valor'].replace('.','').replace(',','.').replace('R$\xa0','').replace('R$',''),
            user = user_logado, usuarios_id = usuario_cliente
            )
        data['gastos_extras'] = gastos_extras
        data['gastos_extras']  = Gastos_extras.objects.filter(
            usuarios_id= usuario_cliente, data_hora__month = mes_atual, data_hora__year=ano ).order_by('-id')
        data['categoria_de_gastos']= GastosExtrasCategoria.objects.filter(
            usuarios_id= usuario_cliente).order_by('-id')
        data['hoje']= hoje
        return render(
             request, 'financeiro/gastos-extras.html',data)

@login_required() 
def gastosExtras_delete(request, id):
    user = request.user.has_perm('financeiro.change_gastos_extras')
    if user == False:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    user_logado = request.user.id
    usuario_cliente = autenticar_usuario(user_logado)
    autorizarcao_de_reistros = autorizarcao_de_reistro(usuario_cliente)
    if autorizarcao_de_reistros:
        return autorizarcao_de_reistros

    data  = {}
    gastos_extras= Gastos_extras.objects.get(id= id)
    usuario_adm = gastos_extras.usuarios.id
    if usuario_adm == usuario_cliente: 
        if request.method == 'POST':
            gastos_extras.delete()
            return redirect('gastos-extras')
        else:
            return render(request, 'financeiro/gastos-extras-delete-confirme.html',data)
    else:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

class GastosExtrasUpdate(LoginRequiredMixin, View):
    def get(self, request, id):
        user = request.user.has_perm('financeiro.change_gastos_extras')
        if user == False:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        data={}
        user_logado = request.user.id
        usuario_cliente = autenticar_usuario(user_logado)
        autorizarcao_de_reistros = autorizarcao_de_reistro(usuario_cliente)
        if autorizarcao_de_reistros:
            return autorizarcao_de_reistros

        gastos_extras= Gastos_extras.objects.get(id= id)
        usuario_adm = gastos_extras.usuarios.id
        if usuario_adm == usuario_cliente: 
            data['categoria_de_gastos']= GastosExtrasCategoria.objects.filter(
                usuarios_id= usuario_cliente).order_by('-id')
            data['gastos_extras']= Gastos_extras.objects.get(id= id)
            return render(
                request, 'financeiro/gastos_extras_update.html', data)
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    def post(self, request, id):
        user = request.user.has_perm('financeiro.change_gastos_extras')
        if user == False:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        user_logado = request.user.id
        usuario_cliente = autenticar_usuario(user_logado)
        autorizarcao_de_reistros = autorizarcao_de_reistro(usuario_cliente)
        if autorizarcao_de_reistros:
            return autorizarcao_de_reistros
      
        gastos_extras= Gastos_extras.objects.get(id= id)
        usuario_adm = gastos_extras.usuarios.id
        if usuario_adm == usuario_cliente: 
            gastos_extras.id= id
            gastos_extras.descricao = request.POST['descricao']
            gastos_extras.gastosExtrasCategoria_id= request.POST['categoria']
            gastos_extras.valor = request.POST['valor'].replace('.','').replace(',','.').replace('R$\xa0','').replace('R$','')
            gastos_extras.user = user_logado
            gastos_extras.save()
            return redirect('gastos-extras')
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

class FiltroGastosExtras( LoginRequiredMixin, View):
    def get(self, request):
        user_logado = request.user.id
        usuario_cliente = autenticar_usuario(user_logado)
        autorizarcao_de_reistros = autorizarcao_de_reistro(usuario_cliente)
        if autorizarcao_de_reistros:
            return autorizarcao_de_reistros

        data={}
        today = date.today()
        mes_atual = today.month
        gastos_extras = Gastos_extras.objects.filter(
            usuarios_id= usuario_cliente, data_hora__month = mes_atual ).order_by('-id')
        mes= request.GET.get('mes',None)
        categoria= request.GET.get('categoria',None)
     
        if mes:
            gastos_extras = Gastos_extras.objects.filter(
                usuarios_id= usuario_cliente, data_hora__contains= mes).order_by('-id')
            data['gastos_extr']= gastos_extras.aggregate(total=Sum('valor'))

        if mes and categoria:
            gastos_extras = Gastos_extras.objects.filter(
                usuarios_id = usuario_cliente, data_hora__contains= mes, gastosExtrasCategoria_id= categoria).order_by('-id')
            data['gastos_extr']= gastos_extras
        
        data['hoje']= today
        data['categoria_de_gastos']= GastosExtrasCategoria.objects.filter(
            usuarios_id= usuario_cliente).order_by('-id')
        data['gastos_extras'] = gastos_extras
        
        return render(
            request, 'financeiro/gastos-extras.html', data)
class Gastos_extras_categoria(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user.has_perm('financeiro.add_gastosextrascategoria')
        if user == False:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        user_logado = request.user.id
        usuario_cliente = autenticar_usuario(user_logado)
        autorizarcao_de_reistros = autorizarcao_de_reistro(usuario_cliente)
        if autorizarcao_de_reistros:
            return autorizarcao_de_reistros
        
        data = {}
        data['categoria_de_gastos']= GastosExtrasCategoria.objects.filter(
            usuarios_id= usuario_cliente).order_by('-id')
        return render(
            request, 'financeiro/categoria_de_gastos.html', data)

    def post(self, request):
        user = request.user.has_perm('financeiro.add_gastosextrascategoria')
        if user == False:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        user_logado = request.user.id
        usuario_cliente = autenticar_usuario(user_logado)
        autorizarcao_de_reistros = autorizarcao_de_reistro(usuario_cliente)
        if autorizarcao_de_reistros:
            return autorizarcao_de_reistros

        categoria = GastosExtrasCategoria.objects.create(
        nome = request.POST['nome'],
        user = user_logado, usuarios_id = usuario_cliente)
        return redirect('categoria_de_gastos')

class GastosExtrasDashboard(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user.has_perm('financeiro.view_relatorios')
        if user == False:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        user_logado = request.user.id
        usuario_cliente = autenticar_usuario(user_logado)
        autorizarcao_de_reistros = autorizarcao_de_reistro(usuario_cliente)
        if autorizarcao_de_reistros:
            return autorizarcao_de_reistros

        data= {}
        periodo= request.GET.get('periodo',None)
        today = date.today()
        ano = str(today.year)
        mes = today.month
        data['dashboard'] = Gastos_extras.objects.filter(
                usuarios_id= usuario_cliente, data_hora__year= ano, data_hora__month= mes).values(
                'gastosExtrasCategoria__nome').annotate(valor =Sum('valor')).order_by('-valor')
        if periodo:
            data['dashboard'] = Gastos_extras.objects.filter(
                usuarios_id = usuario_cliente, data_hora__contains= periodo).values(
                'gastosExtrasCategoria__nome').annotate(valor =Sum('valor')).order_by('-valor')

        return render(request, 'financeiro/dashboard.html', data) 

class Gastos_extras_categoriaUpdate(LoginRequiredMixin, View):
    def get(self, request, id):
        user = request.user.has_perm('financeiro.change_gastosextrascategoria')
        if user == False:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        user_logado = request.user.id
        usuario_cliente = autenticar_usuario(user_logado)
        autorizarcao_de_reistros = autorizarcao_de_reistro(usuario_cliente)
        if autorizarcao_de_reistros:
            return autorizarcao_de_reistros

        data = {}    
        categoria= GastosExtrasCategoria.objects.get(id= id)
        usuario_adm = categoria.usuarios.id
        if usuario_adm == usuario_cliente: 
            data['categoria'] = GastosExtrasCategoria.objects.get(id=id)
            return render(
                request, 'financeiro/categoria_de_gastosUpdate.html', data)
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    def post(self, request, id):
        user = request.user.has_perm('financeiro.add_gastosextrascategoria')
        if user == False:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        user_logado = request.user.id
        usuario_cliente = autenticar_usuario(user_logado)
        autorizarcao_de_reistros = autorizarcao_de_reistro(usuario_cliente)
        if autorizarcao_de_reistros:
            return autorizarcao_de_reistros
  
        categoria = GastosExtrasCategoria.objects.get(id=id)
        categoria.id=id
        categoria.nome = request.POST['nome']
        categoria.user = user_logado
        categoria.save()
        return redirect('gastos-extras')
    
def categoria_de_gastos_delete(request, id):
    user = request.user.has_perm('financeiro.delete_gastosextrascategoria')
    if user == False:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    user_logado = request.user.id
    usuario_cliente = autenticar_usuario(user_logado)
    autorizarcao_de_reistros = autorizarcao_de_reistro(usuario_cliente)
    if autorizarcao_de_reistros:
        return autorizarcao_de_reistros

    data  = {}
    categoria= GastosExtrasCategoria.objects.get(id= id)
    usuario_adm = categoria.usuarios.id
    if usuario_adm == usuario_cliente:
        if request.method == 'POST':
            categoria.delete()
            return redirect('gastos-extras')
        else:
            return render(request, 'financeiro/gastos-extras-delete-confirme.html',data)
    else:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

class ContasAreceber(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user.has_perm('financeiro.add_contas')
        if user == False:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        user_logado = request.user.id
        usuario_cliente = autenticar_usuario(user_logado)
        autorizarcao_de_reistros = autorizarcao_de_reistro(usuario_cliente)
        if autorizarcao_de_reistros:
            return autorizarcao_de_reistros

        today = date.today()
        mes_atual = today.month
        dia = request.GET.get('dia')
        dia2 = request.GET.get('dia2')

        conta = Contas.objects.filter(
            ~Q(parcelas_restantes = 0 ), usuarios_id= usuario_cliente, tipo_de_conta_id=1).order_by('-id')[:20]
        venda= Venda.objects.filter(usuarios_id= usuario_cliente, data_hora__gte = today).order_by('-id')
        cliente = Cliente.objects.filter(usuarios_id= usuario_cliente).order_by('-id')

        client = request.GET.get('client',None)
        nome_cliente = request.GET.get('nome_cliente')
        estado_da_conta = request.GET.get('estado_da_conta',None)

        if estado_da_conta == '1':
            conta = Contas.objects.filter(
                ~Q(parcelas_restantes = 0 ), cliente__cpf_cnpj = client, usuarios_id= usuario_cliente).order_by('-id') # filtrando contas maior que 0
        
        elif estado_da_conta == '2':
            conta = Contas.objects.filter(
                usuarios_id= usuario_cliente, parcelas_restantes = 0, cliente__cpf_cnpj = client ).order_by('-id') #filtrando contas igual a 0
        elif estado_da_conta == '':
            conta = Contas.objects.filter(
                usuarios_id= usuario_cliente, cliente__cpf_cnpj = client ).order_by('-id')

        if dia and dia2: 
            conta = Contas.objects.filter(
                usuarios_id= usuario_cliente, data_de_vencimento__range = (dia, dia2 ), tipo_de_conta_id=1).order_by('-id')
        
        elif nome_cliente:
            conta = Contas.objects.filter(
                usuarios_id= usuario_cliente, cliente__id = nome_cliente ).order_by('-id')
        
        return render(
            request, 'financeiro/conta-areceber.html', {
                'conta': conta, #'tipo_de_conta': tipo_de_conta,
                'venda': venda, 'cliente':cliente, 'client': client,
                })

    def post(self, request):
        user = request.user.has_perm('financeiro.add_contas')
        if user == False:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        user_logado = request.user.id
        usuario_cliente = autenticar_usuario(user_logado)
        autorizarcao_de_reistros = autorizarcao_de_reistro(usuario_cliente)
        if autorizarcao_de_reistros:
            return autorizarcao_de_reistros
        data = {}
        today = date.today()
        mes_atual = today.month
        parcelas = request.POST['parcelas']
        parcelas = int(parcelas)
        data_de_vencimento_parcelas = request.POST['data_de_vencimento']
        data_de_vencimento_parcelas =  datetime.datetime.strptime(data_de_vencimento_parcelas, "%Y-%m-%d")
        ano = data_de_vencimento_parcelas.year
        mes = data_de_vencimento_parcelas.month
        dia = data_de_vencimento_parcelas.day
        parcela=0

        conta = Contas.objects.create(
            observacao = request.POST['observacao'],
            valor = request.POST['valor'].replace('.','').replace(',','.').replace('R$\xa0','').replace('R$',''),
            parcelas = parcelas or 1,
            juros = request.POST['juros'].replace(' ','').replace(',','.') or 0,
            tipo_de_conta_id = request.POST['tipo_de_conta_id'],
            data_de_vencimento = data_de_vencimento_parcelas,
            venda_id = request.POST['venda_id'],
            cliente_id = request.POST['cliente_id'],
            user = user_logado, usuarios_id = usuario_cliente,
            )
        if conta:
            parcelas= conta.parcelas
            id_da_conta = conta.id 
            for conta in range( parcelas):
                parcela= parcela + 1
                if data_de_vencimento_parcelas.month <= 11 :
                    if parcela >= 2:
                        mes = mes + 1
                        data_de_vencimento_parcelas= date(year=ano, month=mes, day=dia)
                elif mes == 12 and parcela <= 1:
                    mes = 12
                    data_de_vencimento_parcelas= date(year=ano, month=mes, day=dia)
                else:
                    mes = mes
                    mes = 1
                    ano = ano + 1
                    dia = dia
                    dia = data_de_vencimento_parcelas.day
                    data_de_vencimento_parcelas= date(year=ano, month=mes, day=dia)
                          
                parcelas = ParcelasConta.objects.create(
                    contas_id = id_da_conta,
                    numero_da_parcelas = parcela,
                    data_de_vencimento = data_de_vencimento_parcelas,
                    user = user_logado, usuarios_id= usuario_cliente,
                )

        data['conta'] = conta
        data['conta']  = Contas.objects.filter(usuarios_id= usuario_cliente, tipo_de_conta_id=1, data_de_vencimento__month = mes_atual).order_by('-id') # listar produtos
        data['venda']  = Venda.objects.filter(usuarios_id= usuario_cliente, data_hora__gte = today).order_by('-id')
        data['cliente'] = Cliente.objects.filter(usuarios_id= usuario_cliente,).order_by('-id')
        return render(
             request, 'financeiro/conta-areceber.html',data)

@login_required()
def conta_delete(request, id):
    user = request.user.has_perm('financeiro.delete_contas')
    if user == False:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    user_logado = request.user.id
    usuario_cliente = autenticar_usuario(user_logado)
    autorizarcao_de_reistros = autorizarcao_de_reistro(usuario_cliente)
    if autorizarcao_de_reistros:
        return autorizarcao_de_reistros

    data  = {}
    conta = Contas.objects.get(id= id)
    usuario_adm = conta.usuarios.id
    if usuario_adm == usuario_cliente: 
        if request.method == 'POST':
            conta.delete()
            return redirect('conta_areceber')
        else:
            return render(request, 'financeiro/conta-delete-confirme.html',data)
    else:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

class ContaAreceberUpdate(LoginRequiredMixin, View):
    def get(self, request, id):
        user = request.user.has_perm('financeiro.change_contas')
        if user == False:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        user_logado = request.user.id
        usuario_cliente = autenticar_usuario(user_logado)
        autorizarcao_de_reistros = autorizarcao_de_reistro(usuario_cliente)
        if autorizarcao_de_reistros:
            return autorizarcao_de_reistros
        
        conta = Contas.objects.get(id= id)
        usuario_adm = conta.usuarios.id
        if usuario_adm == usuario_cliente:
            return render(
                request, 'financeiro/conta_areceber_update.html',{'conta': conta})
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
   
    def post(self, request, id):
        user = request.user.has_perm('financeiro.change_contas')
        if user == False:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        user_logado = request.user.id
        usuario_cliente = autenticar_usuario(user_logado)
        autorizarcao_de_reistros = autorizarcao_de_reistro(usuario_cliente)
        if autorizarcao_de_reistros:
            return autorizarcao_de_reistros
       
        parcelas= int(request.POST['parcelas'])
        if parcelas < 1:
            parcelas = 1
        else:
            parcelas = request.POST['parcelas']
        parcelas = int(parcelas)
        data_de_vencimento_parcelas = request.POST['data_de_vencimento']
        data_de_vencimento_parcelas =  datetime.datetime.strptime(data_de_vencimento_parcelas, "%Y-%m-%d")
        ano = data_de_vencimento_parcelas.year
        mes = data_de_vencimento_parcelas.month
        dia = data_de_vencimento_parcelas.day
       
        conta = Contas.objects.get(id= id)
        usuario_adm = conta.usuarios.id
        if usuario_adm == usuario_cliente: 
            conta.id= id
            conta.observacao = request.POST['observacao']
            if request.POST['valor']:
                conta.valor = request.POST['valor'].replace('.','').replace(',','.').replace('R$\xa0','').replace('R$','')
            conta.parcelas = parcelas or 1
            if request.POST['juros']:
                conta.juros = request.POST['juros'].replace(' ','').replace(',','.')
            conta.tipo_de_conta_id = request.POST['tipo_de_conta_id']
            if request.POST['data_de_vencimento']:
                conta.data_de_vencimento = data_de_vencimento_parcelas
            conta.venda_id = request.POST['venda_id']
            conta.cliente_id = request.POST['cliente_id']
            conta.user = user_logado 
            conta.save()

        if conta:
            parcela_delete = ParcelasConta.objects.filter(contas_id=id)
            parcela_delete.delete()

            parcelas= conta.parcelas
            id_da_conta = conta.id 
            parcela= 0
            parcelas= parcelas - int(conta.parcelas_pagas)
            for conta in range( parcelas):
                parcela= parcela + 1
                if data_de_vencimento_parcelas.month <= 11 :
                    if parcela >= 2:
                        mes = mes + 1
                        data_de_vencimento_parcelas= date(year=ano, month=mes, day=dia)
                elif mes == 12 and parcela <= 1:
                    mes = 12
                    data_de_vencimento_parcelas= date(year=ano, month=mes, day=dia)
                else:
                    mes = mes
                    mes = 1
                    ano = ano + 1
                    dia = dia
                    dia = data_de_vencimento_parcelas.day
                    data_de_vencimento_parcelas= date(year=ano, month=mes, day=dia)
                          
                parcelas = ParcelasConta.objects.create(
                    contas_id = id_da_conta,
                    numero_da_parcelas = parcela,
                    data_de_vencimento = data_de_vencimento_parcelas,
                    user = user_logado, usuarios_id = usuario_cliente
                )
            return redirect('conta_areceber')
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

class ContasApagar(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user.has_perm('financeiro.add_contas')
        if user == False:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

        user_logado = request.user.id
        usuario_cliente = autenticar_usuario(user_logado)
        autorizarcao_de_reistros = autorizarcao_de_reistro(usuario_cliente)
        if autorizarcao_de_reistros:
            return autorizarcao_de_reistros

        today = date.today()
        ano_atual = today.year
        mes_atual = today.month
        prox_5_dias = today.day
        hoje = today.day
        prox_5_dias = date(ano_atual, mes_atual, prox_5_dias)

        conta = Contas.objects.filter(
            usuarios_id= usuario_cliente, tipo_de_conta_id=2).order_by('-id')
        tipo_de_conta = Tipo_de_conta.objects.all()

        Data_vencimento = request.GET.get('data_vencimento',None)
        estado_da_conta = request.GET.get('estado_da_conta',None)

        if estado_da_conta == '':
            conta = Contas.objects.filter(
                ~Q(parcelas_restantes = 0) & Q(tipo_de_conta_id=2 ), usuarios_id= usuario_cliente).order_by('-id')
        elif estado_da_conta == '0':
            conta = Contas.objects.filter(
                usuarios_id= usuario_cliente, parcelas_restantes = 0, tipo_de_conta_id=2).order_by('-id')

        if Data_vencimento == '1':
            conta = Contas.objects.filter(
                usuarios_id= usuario_cliente, data_de_vencimento__month = mes_atual, tipo_de_conta_id=2).order_by('-id')
        elif Data_vencimento == '2':
            conta = Contas.objects.filter(
                usuarios_id= usuario_cliente, data_de_vencimento__range = ( today, prox_5_dias), tipo_de_conta_id=2).order_by('-id')

        elif Data_vencimento == '3':
            conta = Contas.objects.filter(
                usuarios_id= usuario_cliente, data_de_vencimento__day = hoje, tipo_de_conta_id=2 ).order_by('-id')
        return render(
            request, 'financeiro/conta-apagar.html', {
                'conta': conta, 'tipo_de_conta': tipo_de_conta})

    def post(self, request):
        data = {}
        user = request.user.has_perm('financeiro.add_contas')
        if user == False:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        user_logado = request.user.id
        usuario_cliente = autenticar_usuario(user_logado)
        autorizarcao_de_reistros = autorizarcao_de_reistro(usuario_cliente)
        if autorizarcao_de_reistros:
            return autorizarcao_de_reistros 

        parcelas= int(request.POST['parcelas'])
        if parcelas < 1:
            parcelas = 1
        else:
            parcelas = request.POST['parcelas']
        parcelas = int(parcelas)
        data_de_vencimento_parcelas = request.POST['data_de_vencimento']
        data_de_vencimento_parcelas =  datetime.datetime.strptime(data_de_vencimento_parcelas, "%Y-%m-%d")
        ano = data_de_vencimento_parcelas.year
        mes = data_de_vencimento_parcelas.month
        dia = data_de_vencimento_parcelas.day
        parcela=0
        
        conta = Contas.objects.create(
            observacao = request.POST['observacao'],
            valor = request.POST['valor'].replace('.','').replace(',','.').replace('R$\xa0','').replace('R$',''),
            parcelas = parcelas,
            juros = request.POST['juros'].replace(' ','').replace(',','.') or 0,
            tipo_de_conta_id = request.POST['tipo_de_conta_id'],
            data_de_vencimento = data_de_vencimento_parcelas,
            user = user_logado, usuarios_id = usuario_cliente
            )
        if conta:
            parcelas= conta.parcelas
            id_da_conta = conta.id 
            for conta in range( parcelas):
                parcela= parcela + 1
                if data_de_vencimento_parcelas.month <= 11 :
                    if parcela >= 2:
                        mes = mes + 1
                        data_de_vencimento_parcelas= date(year=ano, month=mes, day=dia)
                elif mes == 12 and parcela <= 1:
                    mes = 12
                    data_de_vencimento_parcelas= date(year=ano, month=mes, day=dia)
                else:
                    mes = mes
                    mes = 1
                    ano = ano + 1
                    dia = dia
                    dia = data_de_vencimento_parcelas.day
                    data_de_vencimento_parcelas= date(year=ano, month=mes, day=dia)
                          
                parcelas = ParcelasConta.objects.create(
                    contas_id = id_da_conta,
                    numero_da_parcelas = parcela,
                    data_de_vencimento = data_de_vencimento_parcelas,
                    user = user_logado, usuarios_id = usuario_cliente
                )

        data['conta'] = conta
        data['conta']  = Contas.objects.filter(
            usuarios_id = usuario_cliente, tipo_de_conta_id=2).order_by('-id') 
        return render(
             request, 'financeiro/conta-apagar.html',data)

class ContaApagarUpdate(LoginRequiredMixin, View):
    def get(self, request, id):
        user = request.user.has_perm('financeiro.change_contas')
        if user == False:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

        user_logado = request.user.id
        usuario_cliente = autenticar_usuario(user_logado)
        autorizarcao_de_reistros = autorizarcao_de_reistro(usuario_cliente)
        if autorizarcao_de_reistros:
            return autorizarcao_de_reistros
        
        conta = Contas.objects.get(id= id)
        usuario_adm = conta.usuarios.id
        if usuario_adm == usuario_cliente: 
            return render(request, 'financeiro/conta_apagar_update.html', {'conta': conta})
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    def post(self, request, id):
        user = request.user.has_perm('financeiro.change_contas')
        if user == False:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        user_logado = request.user.id
        usuario_cliente = autenticar_usuario(user_logado)
        autorizarcao_de_reistros = autorizarcao_de_reistro(usuario_cliente)
        if autorizarcao_de_reistros:
            return autorizarcao_de_reistros
        
        parcelas= int(request.POST['parcelas'])
        if parcelas < 1:
            parcelas = 1
        else:
            parcelas = request.POST['parcelas']
        parcelas = int(parcelas)
        data_de_vencimento_parcelas = request.POST['data_de_vencimento']
        data_de_vencimento_parcelas =  datetime.datetime.strptime(data_de_vencimento_parcelas, "%Y-%m-%d")
        ano = data_de_vencimento_parcelas.year
        mes = data_de_vencimento_parcelas.month
        dia = data_de_vencimento_parcelas.day

        conta = Contas.objects.get(id= id)
        usuario_adm = conta.usuarios.id
        if usuario_adm == usuario_cliente: 
            conta.id= id
            conta.observacao = request.POST['observacao']
            if request.POST['valor']:
                conta.valor = request.POST['valor'].replace('.','').replace(',','.').replace('R$\xa0','').replace('R$','')
            conta.parcelas = parcelas or 1
            if request.POST['juros']:
                conta.juros = request.POST['juros'].replace(' ','').replace(',','.')
            conta.tipo_de_conta_id = request.POST['tipo_de_conta_id']
            if request.POST['data_de_vencimento']:
                conta.data_de_vencimento = data_de_vencimento_parcelas
            conta.user = user_logado
            conta.save()
        
        if conta:
            parcela_delete = ParcelasConta.objects.filter(contas_id=id)
            parcela_delete.delete()

            parcelas= conta.parcelas
            id_da_conta = conta.id 
            parcela= 0
            parcelas= parcelas - int(conta.parcelas_pagas)
            for conta in range( parcelas):
                parcela= parcela + 1
                if data_de_vencimento_parcelas.month <= 11 :
                    if parcela >= 2:
                        mes = mes + 1
                        data_de_vencimento_parcelas= date(year=ano, month=mes, day=dia)
                elif mes == 12 and parcela <= 1:
                    mes = 12
                    data_de_vencimento_parcelas= date(year=ano, month=mes, day=dia)
                else:
                    mes = 1
                    ano = ano + 1
                    dia = dia
                    dia = data_de_vencimento_parcelas.day
                    data_de_vencimento_parcelas= date(year=ano, month=mes, day=dia)
                          
                parcelas = ParcelasConta.objects.create(
                    contas_id = id_da_conta,
                    numero_da_parcelas = parcela,
                    data_de_vencimento = data_de_vencimento_parcelas,
                    user = user_logado, usuarios_id = usuario_cliente
                )
            return redirect('conta_apagar')
        
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

@login_required()
def conta_apagar_delete(request, id):
    user = request.user.has_perm('financeiro.delete_contas')
    if user == False:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    user_logado = request.user.id
    usuario_cliente = autenticar_usuario(user_logado)
    autorizarcao_de_reistros = autorizarcao_de_reistro(usuario_cliente)
    if autorizarcao_de_reistros:
        return autorizarcao_de_reistros

    data  = {} 
    conta = Contas.objects.get(id= id)
    usuario_adm = conta.usuarios.id
    if usuario_adm == usuario_cliente:
        if request.method == 'POST':
            conta.delete()
            return redirect('conta_apagar')
        else:
            return render(request, 'financeiro/conta-delete-confirme.html',data)
    else:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

class Pagamentos(LoginRequiredMixin, View):
    def get(self, request, id):
        user = request.user.has_perm('financeiro.add_pagamento')
        if user == False:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        user_logado = request.user.id
        usuario_cliente = autenticar_usuario(user_logado)
        autorizarcao_de_reistros = autorizarcao_de_reistro(usuario_cliente)
        if autorizarcao_de_reistros:
            return autorizarcao_de_reistros

        conta = Contas.objects.get(id= id)
        usuario_adm = conta.usuarios.id
        if usuario_adm == usuario_cliente:
            data = {}
            parcelas = Contas.objects.get(id=id)
            pagamentos = Pagamento.objects.filter(usuarios_id= usuario_cliente, contas_id = id).order_by('-id')
            parcela = int(parcelas.parcelas_restantes) + 1
            parcela = list(range(parcela))

            data['parcela'] = parcela
            data['conta'] = Contas.objects.get(id=id)
            data['pagamentos'] = pagamentos
            return render(
                request, 'financeiro/pagamento.html',data)
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    def post(self, request, id):
        user = request.user.has_perm('financeiro.add_pagamento')
        if user == False:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        data = {}
        user_logado = request.user.id
        usuario_cliente = autenticar_usuario(user_logado)
        autorizarcao_de_reistros = autorizarcao_de_reistro(usuario_cliente)
        if autorizarcao_de_reistros:
            return autorizarcao_de_reistros 
        conta = Contas.objects.get(id= id)
        perc_restantes = int(conta.parcelas_restantes)
        usuario_adm = conta.usuarios.id
        if usuario_adm == usuario_cliente: 
            if perc_restantes >= 1 :
                pagamento = Pagamento.objects.create(
                    observacao = request.POST['observacao'],
                    quantidade_de_parcelas = 1,
                    contas_id = id, user = user_logado, usuarios_id = usuario_cliente
                    )
                if pagamento:
                    parcela_delete = ParcelasConta.objects.filter(contas_id=id)
                    parcela_delete = parcela_delete.last()
                    parcela_delete.delete()
                    
            else:
                data['mensagem_de_erro'] = 'Você pode ter enviado o número  ( 0 ) ou um valor superior a quantidade de parcelas existente'
                data['conta'] = Contas.objects.get(id=id)
                data['pagamentos'] = Pagamento.objects.filter(
                    usuarios_id= usuario_cliente, contas_id = id).order_by('-id')
    
                return render(
                    request, 'financeiro/pagamento.html',data)
            data['pagamentos'] = Pagamento.objects.filter(
                usuarios_id= usuario_cliente, contas_id = id).order_by('-id')
            data['conta'] = Contas.objects.get(id=id)
            return render(
                request, 'financeiro/pagamento.html',data)
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))


class Parcelas(LoginRequiredMixin, View):
    def get(self, request, id):
        user_logado = request.user.id
        usuario_cliente = autenticar_usuario(user_logado)
        autorizarcao_de_reistros = autorizarcao_de_reistro(usuario_cliente)
        if autorizarcao_de_reistros:
            return autorizarcao_de_reistros
        data={}
        data['empresa'] = usuario_cliente
        data['parcelas']= ParcelasConta.objects.filter(
            contas_id=id, contas__usuarios_id=usuario_cliente)
        data['conta'] = Contas.objects.get(id=id)
        return render(
            request, 'financeiro/parcelas.html', data)


class Relarorio_produtos(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user.has_perm('financeiro.view_relatorios')
        if user == False:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        user_logado = request.user.id
        usuario_cliente = autenticar_usuario(user_logado)
        autorizarcao_de_reistros = autorizarcao_de_reistro(usuario_cliente)
        if autorizarcao_de_reistros:
            return autorizarcao_de_reistros

        today = date.today()
        ano_atual = str(today.year)
        mes_atual = today.month
        item_de_pedido = ItemDoPedido.objects.filter(
                usuarios_id= usuario_cliente, venda__data_hora__year= ano_atual, venda__data_hora__month= mes_atual ).values(
                'produto__id', 'produto__nome', 'produto__saida').annotate(lucro_obtido=Sum(F(
                        'produto__valor_venal') * F('quantidade_de_itens') - F('produto__valor_compra') * F('quantidade_de_itens'))).annotate(
                            total_investimento=Sum(F('produto__valor_compra') * F('quantidade_de_itens'))).annotate(total_venda=Sum(
                            F('produto__valor_venal') * F('quantidade_de_itens')))

        mes= request.GET.get('mes',None)
        filtro= request.GET.get('filtrar_produto',None)
        if mes:
            item_de_pedido = ItemDoPedido.objects.filter(
                usuarios_id = usuario_cliente, venda__data_hora__contains= mes ).values(
                'produto__id', 'produto__nome', 'produto__saida').annotate(lucro_obtido=Sum(F(
                        'produto__valor_venal') * F('quantidade_de_itens') - F('produto__valor_compra') * F('quantidade_de_itens'))).annotate(
                            total_investimento=Sum(F('produto__valor_compra') * F('quantidade_de_itens'))).annotate(total_venda=Sum(
                            F('produto__valor_venal') * F('quantidade_de_itens'))).order_by(filtro)
        return render(
            request, 'financeiro/relatorio-produtos.html', {
                'item_de_pedido': item_de_pedido, 
                'ano_atual':ano_atual, 
                'mes_atual': mes_atual
                })

class Relatorio_diario(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user.has_perm('financeiro.view_relatorios')
        if user == False:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        user_logado = request.user.id
        usuario_cliente = autenticar_usuario(user_logado)
        autorizarcao_de_reistros = autorizarcao_de_reistro(usuario_cliente)
        if autorizarcao_de_reistros:
            return autorizarcao_de_reistros

        today = date.today()
        dia= request.GET.get('dia',None)
        if dia == None:
            dia= today
        invertimento_do_dia = ItemDoPedido.objects.filter(
            usuarios_id= usuario_cliente, venda__data_hora__contains= dia ).aggregate(
                total_invertimento=Sum(F('produto__valor_compra') * F('quantidade_de_itens')))
        invertimento_do_dia = invertimento_do_dia['total_invertimento'] or 0

        vendas_do_dia = Venda.objects.filter(
            usuarios_id= usuario_cliente, data_hora__contains= dia ).aggregate(total_venda=Sum('valor'))
        vendas_do_dia = vendas_do_dia['total_venda']or 0

        cedula = Venda.objects.filter(
            usuarios_id= usuario_cliente, data_hora__contains= dia ).aggregate(total_venda_cedula=Sum('valor_cedula'))

        credito = Venda.objects.filter(
            usuarios_id= usuario_cliente, data_hora__contains= dia).aggregate(total_venda_credito=Sum('valor_credito'))

        debito = Venda.objects.filter(
           usuarios_id= usuario_cliente, data_hora__contains= dia).aggregate(total_venda_debito=Sum('valor_debito'))

        lucro_diario = vendas_do_dia - invertimento_do_dia

        desconto_po_dia = Venda.objects.filter(
            usuarios_id= usuario_cliente, data_hora__contains= dia ).aggregate(total_desconto=Sum('total_desconto'))


        gastos_extras_diario = Gastos_extras.objects.filter(
            usuarios_id= usuario_cliente, data_hora__contains=dia ).aggregate(gastos = Sum('valor'))

        Contas_diario_a_receber = ParcelasConta.objects.filter(
            usuarios_id= usuario_cliente, data_de_vencimento__contains=dia, contas__tipo_de_conta__id=1).aggregate(total_conta = Sum('contas__valor_parcela'))

        Contas_diario_a_pagar = ParcelasConta.objects.filter(
            usuarios_id= usuario_cliente, data_de_vencimento__contains=dia, contas__tipo_de_conta__id=2).aggregate(total_conta = Sum('contas__valor_parcela'))

        return render(
                request, 'financeiro/relatorio-diario.html', {
                    'invertimento_do_dia': invertimento_do_dia,
                    'vendas_do_dia': vendas_do_dia,
                    'lucro_diario': lucro_diario,
                    'gastos_extras_diario': gastos_extras_diario,
                    'desconto_po_dia':desconto_po_dia,
                    'today':today,
                    'cedula':cedula,
                    'credito':credito,
                    'debito':debito,
                    'Contas_diario_a_receber': Contas_diario_a_receber,
                    'Contas_diario_a_pagar':Contas_diario_a_pagar,
                    })


class Relatorio_mensal(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user.has_perm('financeiro.view_relatorios')
        if user == False:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        user_logado = request.user.id
        usuario_cliente = autenticar_usuario(user_logado)
        autorizarcao_de_reistros = autorizarcao_de_reistro(usuario_cliente)
        if autorizarcao_de_reistros:
            return autorizarcao_de_reistros

        today = date.today()
        ano_atual = today.year
        mes = today.month
        mess= request.GET.get('mes',None)

        invertimento = ItemDoPedido.objects.filter(
            usuarios_id= usuario_cliente, venda__data_hora__month= mess, venda__data_hora__year= ano_atual ).aggregate(
                total_invertimento=Sum(F('produto__valor_compra') * F('quantidade_de_itens')))
        valor_invertimento = invertimento['total_invertimento'] or 0

        vendas = Venda.objects.filter(
            usuarios_id= usuario_cliente, data_hora__month= mess, data_hora__year= ano_atual ).aggregate(total_venda=Sum('valor'))
        valor_venda = vendas['total_venda']or 0

        cedula = Venda.objects.filter(
            usuarios_id= usuario_cliente, data_hora__month= mess, data_hora__year= ano_atual ).aggregate(total_venda_cedula=Sum('valor_cedula'))

        credito = Venda.objects.filter(
            usuarios_id= usuario_cliente, data_hora__month= mess, data_hora__year= ano_atual).aggregate(total_venda_credito=Sum('valor_credito'))

        debito = Venda.objects.filter(
            usuarios_id= usuario_cliente, data_hora__month= mess, data_hora__year= ano_atual).aggregate(total_venda_debito=Sum('valor_debito'))

        lucro_mensal = valor_venda - valor_invertimento

        gastos_extras = Gastos_extras.objects.filter(
            usuarios_id= usuario_cliente, data_hora__month= mess, data_hora__year= ano_atual ).aggregate(gastos =Sum('valor'))

        desconto_po_mes = Venda.objects.filter(
            usuarios_id= usuario_cliente, data_hora__month= mess, data_hora__year= ano_atual ).aggregate(total_desconto=Sum('total_desconto'))

        Contas_mensal_a_receber = ParcelasConta.objects.filter(
            usuarios_id= usuario_cliente, data_de_vencimento__month= mess, contas__tipo_de_conta__id=1, data_de_vencimento__year= ano_atual).aggregate(total_conta = Sum('contas__valor_parcela'))

        Contas_mensal_a_pagar = ParcelasConta.objects.filter(
            usuarios_id= usuario_cliente, data_de_vencimento__month= mess, contas__tipo_de_conta__id=2, data_de_vencimento__year= ano_atual).aggregate(total_conta = Sum('contas__valor_parcela'))

        return render(request, 'financeiro/relatorio-mensal.html', {
            'vendas': vendas,
            'invertimento': invertimento,
            'lucro_mensal': lucro_mensal,
            'gastos_extras': gastos_extras,
            'Contas_mensal_a_receber':Contas_mensal_a_receber,
            'Contas_mensal_a_pagar':Contas_mensal_a_pagar,
            'desconto_po_mes':desconto_po_mes,
            'MES': mes,
            'cedula':cedula,
            'credito':credito,
            'debito':debito,
            })


class Relatorio_anual(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user.has_perm('financeiro.view_relatorios')
        if user == False:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        user_logado = request.user.id
        usuario_cliente = autenticar_usuario(user_logado)
        autorizarcao_de_reistros = autorizarcao_de_reistro(usuario_cliente)
        if autorizarcao_de_reistros:
            return autorizarcao_de_reistros

        today = date.today()
        ano_atual = today.year
        ano_atual=str(ano_atual)
        ano= request.GET.get('ano',None)

        venda_desse_ano = Venda.objects.filter(
            usuarios_id= usuario_cliente, data_hora__year=ano ).aggregate(total_venda=Sum('valor'))
        venda_desse_ano = venda_desse_ano['total_venda']or 0

        cedula = Venda.objects.filter(
            usuarios_id= usuario_cliente, data_hora__year= ano ).aggregate(total_venda_cedula=Sum('valor_cedula'))

        credito = Venda.objects.filter(
            usuarios_id= usuario_cliente, data_hora__year= ano ).aggregate(total_venda_credito=Sum('valor_credito'))

        debito = Venda.objects.filter(
            usuarios_id= usuario_cliente, data_hora__year= ano).aggregate(total_venda_debito=Sum('valor_debito'))

        invertimento_anual = ItemDoPedido.objects.filter(
            usuarios_id= usuario_cliente, venda__data_hora__year=ano ).aggregate(
                total_invertimento=Sum(F('produto__valor_compra') * F('quantidade_de_itens')))
        invertimento_anual = invertimento_anual['total_invertimento'] or 0

        lucro_anual= venda_desse_ano - invertimento_anual

        gastos_extras_anual = Gastos_extras.objects.filter(
            usuarios_id= usuario_cliente, data_hora__year=ano ).aggregate(gastos = Sum('valor'))

        desconto_po_anual = Venda.objects.filter(
            usuarios_id= usuario_cliente, data_hora__year= ano ).aggregate(total_desconto=Sum('total_desconto'))

        Contas_anual_a_receber = ParcelasConta.objects.filter(
            usuarios_id= usuario_cliente, data_de_vencimento__year= ano, contas__tipo_de_conta__id=1).aggregate(total_conta = Sum('contas__valor_parcela'))

        Contas_anual_a_pagar = ParcelasConta.objects.filter(
            usuarios_id= usuario_cliente, data_de_vencimento__year= ano, contas__tipo_de_conta__id=2).aggregate(total_conta = Sum('contas__valor_parcela'))

        return render(
                request, 'financeiro/relatorio-anual.html', {
                    'venda_desse_ano':venda_desse_ano,
                    'invertimento_anual': invertimento_anual,
                    'lucro_anual': lucro_anual,
                    'gastos_extras_anual':gastos_extras_anual,
                    'desconto_po_anual': desconto_po_anual,
                    'Contas_anual_a_receber':Contas_anual_a_receber,
                    'Contas_anual_a_pagar':Contas_anual_a_pagar,
                    'cedula':cedula,
                    'credito':credito,
                    'debito':debito,
                    'ano_atual':ano_atual,
                    })

class Fatura(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user.has_perm('financeiro.view_relatorios')
        if user == False:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        user_logado = request.user.id
        usuario_cliente = autenticar_usuario(user_logado)
        autorizarcao_de_reistros = autorizarcao_de_reistro(usuario_cliente)
        if autorizarcao_de_reistros:
            return autorizarcao_de_reistros
        
        registros = registro_de_dados(usuario_cliente, )
        registros['cobranca'] = Cobranca.objects.filter(usuarios = usuario_cliente)
        return render( request, 'financeiro/fatura.html', registros)

