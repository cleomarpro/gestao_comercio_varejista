
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
from usuarios.permitir_autorizar import autenticar_usuario, autorizarcao_de_reistro, registro_de_dados

class NovoUsuario(View):
    def get(self, request):

        return render(
            request, 'novo-usuario.html')

    def post(self, request):
        data = {}
        data['password'] = request.POST['password']
        data['username'] = request.POST['username']
        data['email'] = request.POST['email']

        usuario = User.objects.filter(username= request.POST['username'])or 0
        if usuario != 0:
            data['mensagen_de_erro_usuario'] = 'Usuário já existe!'
            return render(
                request, 'novo-usuario.html', data)
        email = User.objects.filter(email= request.POST['email'])or 0
        if email != 0:
            data['mensagen_de_erro_email'] = 'E-mail já existe!'
            return render(
                request, 'novo-usuario.html', data)
        else:
            usuario = User.objects.create_user(
                password= request.POST['password'],
                username= request.POST['username'],
                email= request.POST['email']
                )
            permissao= Group.objects.get(name='Administrador') 
            permissao_add= usuario.groups.add(permissao)
            cliente = usuario.id 
            novo_usuario = Usuarios.objects.create(
                usuario_cliente= cliente, user_id= cliente, plano_id= 1,
                cpf_cnpj= request.POST['cpf_cnpj'],
                nome_fantazia= request.POST['nome_fantazia'])
            data['usuario'] = usuario
            data['novo_usuario'] = novo_usuario
            return redirect('login')

class UpdateUsuario(LoginRequiredMixin, View):
    def get(self, request):
        user_logado = request.user.id
        usuario = Usuarios.objects.get(user_id = user_logado)
        return render(request,'update-usuario.html', {'usuario': usuario})
    
    def post(self, request):
        user_logado = request.user.id
        usuario = Usuarios.objects.get(user_id = user_logado)
        
        usuario.id= usuario.id
        usuario.cpf_cnpj= request.POST['cpf_cnpj']
        #user= request.POST['user']
        #usuario_cliente= request.POST['usuario_cliente']
        #usuario.plano= request.POST['plano']
        usuario.razao_social= request.POST['razao_social']
        usuario.inscricao_estadual= request.POST['inscricao_estadual']
        usuario.inscricao_municipal= request.POST['inscricao_municipal']
        usuario.nascionalidade= request.POST['nascionalidade']
        usuario.cep= request.POST['cep']
        usuario.rua= request.POST['rua']
        usuario.quadra= request.POST['quadra']
        usuario.numero= request.POST['numero']
        usuario.setor= request.POST['setor']
        usuario.estado= request.POST['estado']
        usuario.cidade= request.POST['cidade']
        usuario.pais= request.POST['pais']
        usuario.complemento= request.POST['complemento']
        #usuario.DDD= request.POST['DDD']
        usuario.Celular= request.POST['Celular']
        #DDD= request.POST['DDD']
        usuario.Telefone= request.POST['Telefone']
        usuario.email= request.POST['email']
        usuario.nome_fantazia= request.POST['nome_fantazia']
        if request.POST['data_de_criacao']:
            usuario.data_de_criacao= request.POST['data_de_criacao']
        #data_hora= request.POST['data_hora']
        usuario.save()

        userLogado = request.user
        userLogado.email= request.POST['email'] # alterando o email do usuário logado
        userLogado.save()
        return redirect('usuario')
        
class MeuPlano(View):
    def get(self, request):
        user_logado = request.user.id
        usuario_cliente = autenticar_usuario(user_logado)

        usuario = Usuarios.objects.get(id = usuario_cliente)
        data = {}
        usuario_cliente = autenticar_usuario(user_logado)
        data['registro_de_dados'] = registro_de_dados(usuario_cliente)
        data['meu_plano'] = usuario.plano.id
        return render(request, 'plano.html', data)
    def post(self, request):
        user_logado = request.user.id
        usuario_cliente = autenticar_usuario(user_logado)

        usuario = Usuarios.objects.get(id = usuario_cliente)
        #usuario.id = user_logado
        usuario.plano_id= request.POST['plano']
        usuario.save()
        data = {}
        usuario_cliente = autenticar_usuario(user_logado)
        data['registro_de_dados'] = registro_de_dados(usuario_cliente)
        data['meu_plano'] = usuario.plano.id
        return render(request, 'plano.html', data)

class NovoFuncionario(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user.has_perm('pessoa.add_funcionario')
        if user == False:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        user_logado = request.user.id
        usuario_cliente = autenticar_usuario(user_logado)
        autorizarcao_de_reistros = autorizarcao_de_reistro(usuario_cliente)
        if autorizarcao_de_reistros:
            return autorizarcao_de_reistros

        usuarios= Funcionario.objects.filter(usuarios_id= usuario_cliente)
        return render(
            request, 'novo-funcionario.html',{'usuarios': usuarios })

    def post(self, request):
        user = request.user.has_perm('pessoa.add_funcionario')
        if user == False:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        user_logado = request.user.id
        usuario_cliente = autenticar_usuario(user_logado)
        autorizarcao_de_reistros = autorizarcao_de_reistro(usuario_cliente)
        if autorizarcao_de_reistros:
            return autorizarcao_de_reistros

        data = {}
        username = User.objects.filter(username= request.POST['username'])or 0
        if username != 0:
            data['mensagen_de_erro_usuario'] = 'Usuário já existe!'
            return render(
                request, 'novo-funcionario.html', data)
        else:
            usuario = User.objects.create_user(
                password= request.POST['password'],
                username= request.POST['username'],
                #email= request.POST['email'],
                first_name= request.POST['primeiro_nome'],
                last_name= request.POST['segundo_nome'],
                is_active= request.POST['ativo']
                )
            permissaos= Group.objects.get(name= request.POST['permissao']) 
            permissao_add= usuario.groups.add(permissaos)
    
            usuario= usuario.id 
            funcionario = Funcionario.objects.create(
                usuarios_id = usuario_cliente, user_id= usuario,
                nome= request.POST['primeiro_nome'],
                segundo_nome= request.POST['segundo_nome'],
                )
            data['usuario'] = usuario
            data['funcionario'] = funcionario
            data['usuarios']= Funcionario.objects.filter(usuarios_id= usuario_cliente)
            return render(
                request, 'novo-funcionario.html', data)

class UpdateFuncionario(LoginRequiredMixin, View):
    def get(self, request, id):
        user = request.user.has_perm('pessoa.change_funcionario')
        if user == False:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        user_logado = request.user.id
        usuario_cliente = autenticar_usuario(user_logado)
        autorizarcao_de_reistros = autorizarcao_de_reistro(usuario_cliente)
        if autorizarcao_de_reistros:
            return autorizarcao_de_reistros

        funcionarios = Funcionario.objects.get(user__id = id)
        usuario_adm = funcionarios.usuarios.usuario_cliente
        if  usuario_adm == usuario_cliente:
            data = {}
            usuario= User.objects.get(id= id)
            data['usuario'] = usuario
            data['permissoes'] = usuario.groups.all()
            data['usuarioCliente'] = usuario_cliente
            return render(
                    request, 'update-funcionario.html', data)
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    def post(self, request, id):
        user = request.user.has_perm('pessoa.change_funcionario')
        if user == False:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        user_logado = request.user.id
        usuario_cliente = autenticar_usuario(user_logado)
        autorizarcao_de_reistros = autorizarcao_de_reistro(usuario_cliente)
        if autorizarcao_de_reistros:
            return autorizarcao_de_reistros

        data = {}
        usuario= User.objects.get(id= id)
        user_atualizado= request.POST['username']
        user_antigo= usuario.username
        senha= request.POST['password']
        usuario_exit = User.objects.filter(username= user_atualizado)or 0
        funcionarios = Funcionario.objects.get(user__id = id)
        usuario_adm = funcionarios.usuarios.usuario_cliente
        if  usuario_adm == usuario_cliente:
            if request.POST['password'] != '123':
                usuario.set_password(senha)
            if user_atualizado != user_antigo:
                if usuario_exit != 0:
                    data['usuario'] = usuario
                    data['permissoes'] = usuario.groups.all()
                    data['mensagen_de_erro_usuario'] = 'Usuário já existe!'
                    return render(
                        request, 'update-funcionario.html', data)
                usuario.username= user_atualizado
            usuario.id = id
            usuario.first_name= request.POST['primeiro_nome']
            usuario.last_name= request.POST['segundo_nome']
            usuario.is_active= request.POST['ativo']
            usuario.save()
            if request.POST['permissao']:
                permissao= Group.objects.get(name= request.POST['permissao']) 
                permissao_add= usuario.groups.add(permissao)
            if request.POST['permissao_delete']:   
                permissao= Group.objects.get(name= request.POST['permissao_delete']) 
                permissao_delete= usuario.groups.remove(permissao)
            data['usuario'] = usuario
            data['permissoes'] = usuario.groups.all()
            return redirect('novo-funcionario')
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

@login_required()
def funcionarioDelete(request, id):
    user = request.user.has_perm('pessoa.delete_funcionario')
    if user == False:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    user_logado = request.user.id
    usuario_cliente = autenticar_usuario(user_logado)
    autorizarcao_de_reistros = autorizarcao_de_reistro(usuario_cliente)
    if autorizarcao_de_reistros:
        return autorizarcao_de_reistros
        
    funcionarios = Funcionario.objects.get(user__id = id)
    usuario_adm = funcionarios.usuarios.usuario_cliente
    if  usuario_adm == usuario_cliente:
        
        data  = {}
        usuario= User.objects.get(id= id)
        if request.method == 'POST':
            usuario.delete()
            return redirect('novo-funcionario')
        else:
            return render(request, 'delete-funcionario.html',data)
    else:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

class Cobrancas(LoginRequiredMixin, View):
    def get(self, request, id):
        user = request.user.has_perm('cobranca.view_cobranca')
        if user == False:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

        usuario_celecionado = Usuarios.objects.get(id = id)
        usuario_celecionado = usuario_celecionado.id
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
                usuarios__usuario_cliente= usuario_celecionado, data_hora__month= Mes, data_hora__year= ano_atual ).aggregate(count= Count('id'))
            vendas = vendas['count'] or 0

            item_do_pedito = ItemDoPedido.objects.filter(
                usuarios__usuario_cliente= usuario_celecionado, venda__data_hora__month= Mes, venda__data_hora__year= ano_atual ).aggregate(count= Count('id'))
            item_do_pedito = item_do_pedito['count'] or 0
            
            Contas_a_receber = Contas.objects.filter(
                usuarios__usuario_cliente= usuario_celecionado, data_hora__month= Mes, tipo_de_conta__id=1, data_hora__year= ano_atual).aggregate(count= Sum('parcelas'))
            Contas_a_receber = Contas_a_receber['count'] or 0

            Contas_a_pagar = Contas.objects.filter(
                usuarios__usuario_cliente= usuario_celecionado, data_hora__month= Mes, tipo_de_conta__id=2, data_hora__year= ano_atual).aggregate(count= Sum('parcelas'))
            Contas_a_pagar = Contas_a_pagar['count'] or 0

            gastos_extras = Gastos_extras.objects.filter(
                usuarios__usuario_cliente= usuario_celecionado, data_hora__month= Mes, data_hora__year= ano_atual).aggregate(count= Count('id'))
            gastos_extras = gastos_extras['count'] or 0

            entrada_de_mercadoria = EntradaMercadoria.objects.filter(
                usuarios__usuario_cliente= usuario_celecionado, data_hora__month= Mes, data_hora__year= ano_atual).aggregate(count= Count('id'))
            entrada_de_mercadoria = entrada_de_mercadoria['count'] or 0

            caixa= Depositar_sacar.objects.filter(usuarios__usuario_cliente= usuario_celecionado, data_hora__month= Mes, data_hora__year= ano_atual).aggregate(count= Count('id'))
            caixa = caixa['count'] or 0

            total_de_registros= vendas + item_do_pedito + Contas_a_receber + Contas_a_pagar + entrada_de_mercadoria + gastos_extras + caixa
            
            if total_de_registros <= 750:
                total_a_pagar = total_de_registros * 4 / 100
                
            else:
                total_a_pagar = total_de_registros * 2 / 100
                total_a_pagar = total_a_pagar + 15
                
            if total_de_registros <= 125:
                fatura= 0
            else:
                fatura= total_a_pagar
                
            data['usuario']= Usuarios.objects.get(id=id)
            data['total_de_registros']= total_de_registros
            data['today']= today
            data['fatura']= fatura
            data['data_atual'] = data_atual
            data['cobranca'] = Cobranca.objects.filter(usuarios__id= id).order_by('-id')
        return render(
            request, 'cobranca.html', data)

    def post(self, request, id):
        user = request.user.has_perm('cobranca.add_cobranca')
        if user == False:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

        data = {}
        today = date.today()
        ano_atual = today.year
        MES = today.month
        mes = MES - 1
        dia = 10
        data_atual= date(day=dia, month=MES, year=ano_atual)
        mes_referente = date(day=dia, month=mes, year=ano_atual)

        Cobranca.objects.create(
            registros= request.POST['registros'],
            valor = request.POST['valor'].replace(',','.'),
            mes_referente = mes_referente,
            data_de_vencimento = data_atual,
            estado_do_debito = request.POST['estado'],
            link_de_cobranca = request.POST['link'],
            usuarios_id =  request.POST['usuario'],
            )
        data['usuario']= Usuarios.objects.get(id=id)
        data['cobranca'] = Cobranca.objects.filter(usuarios__id= id).order_by('-id')
        return render(
            request, 'cobranca.html', data)

class CobrancaUpdate(LoginRequiredMixin, View):
    def get(self, request, id):
        data ={}
        user = request.user.has_perm('cobranca.change_cobranca')
        if user == False:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
       
        data['cobranca'] = Cobranca.objects.get(id= id)
        return render(
            request, 'cobranca-update.html', data)

    def post(self, request, id):
        user = request.user.has_perm('cobranca.change_cobranca')
        if user == False:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
       
        cobranca = Cobranca.objects.get(id=id)
        cobranca.id = id
        cobranca.estado_do_debito = request.POST['estado']
        cobranca.link_de_cobranca = request.POST['link']
        cobranca.save()
        return redirect('usuarios')
    
class Usuario(LoginRequiredMixin, View):
    def get(self, request):
        data ={}
        user = request.user.has_perm('usuarios.view_usuarios')
        if user == False:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

        today = date.today()
        ano_atual = today.year
        Mes = today.month
        data_de_vencimento = request.GET.get('data_de_vencimento') or str(ano_atual)+'-'+ str(Mes)
        if data_de_vencimento !=None:
            data_de_vencimento =  datetime.datetime.strptime(data_de_vencimento, "%Y-%m")
            Mes = data_de_vencimento.month
            ano_atual = data_de_vencimento.year
       
        stado_do_usuario = request.GET.get('estado')
        if stado_do_usuario == 'Pago':
            data['cobranca']= Cobranca.objects.filter(
                estado_do_debito=stado_do_usuario, data_de_vencimento__month= Mes, data_de_vencimento__year= ano_atual)

        elif stado_do_usuario == 'Pedente':
            data['cobranca']= Cobranca.objects.filter(
                estado_do_debito=stado_do_usuario, data_de_vencimento__month= Mes, data_de_vencimento__year= ano_atual)  

        elif stado_do_usuario == 'Cancelado':
            data['cobranca']= Cobranca.objects.filter(
                estado_do_debito=stado_do_usuario, data_de_vencimento__month= Mes, data_de_vencimento__year= ano_atual)
        
        elif stado_do_usuario == 'sem_cobranca':
            data['cobranca']= Cobranca.objects.filter(
                estado_do_debito=stado_do_usuario, data_de_vencimento__month= Mes, data_de_vencimento__year= ano_atual)
        
        elif stado_do_usuario == 'Ativos':
            data['cobranca']= Cobranca.objects.filter(
                estado_do_debito=stado_do_usuario, data_de_vencimento__month= Mes, data_de_vencimento__year= ano_atual)

        else: 
            data['usuario']= Usuarios.objects.all()
        
        return render(
            request, 'usuarios.html', data)

