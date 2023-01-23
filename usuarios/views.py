
from datetime import date
import datetime
from django.contrib.auth.models import User
from django.db.models.aggregates import Count, Sum
from financeiro.models import Contas, Gastos_extras
from fluxo_de_caixa.models import Depositar_sacar, ItemDoPedido, Venda
from pessoa.models import Funcionario
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
        data['plano'] = Plano.objects.all()
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
        data['plano'] = Plano.objects.all()
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
    def get(self, request):
        data={}
        data['cobranca'] = Cobranca.objects.all().order_by('-id')
        return render(
            request, 'cobrancas.html', data)
        
@login_required()
def funcionarioDelete(request,id):
    user = request.user.has_perm('cobranca.view_cobranca')
    if user == False:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    data  = {}
    cobranca = Cobranca.objects.get(id=id)
    if request.method == 'POST':
        cobranca.delete()
        return redirect('cobrancas')
    else:
        return render(request, 'delete-cobrancas.html',data)

class NovaCobrancas(LoginRequiredMixin, View): 
    def get(self, request, id):
        user = request.user.has_perm('cobranca.view_cobranca')
        if user == False:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        data = {}
        today = date.today()
        mes = today.month
        ano = today.year
        if mes > 1 and mes <= 12:
            um_mes_atras = mes - 1
        else:
            um_mes_atras = 12
            um_ano_atras = ano -1
       
        data['usuario']= Usuarios.objects.get(id= id)
        data['registro_de_dados'] = registro_de_dados( id, um_mes_atras, um_ano_atras)
        data['cobranca'] = Cobranca.objects.filter(usuarios__id= id).order_by('-id')
        return render(
            request, 'cobranca.html', data)

    def post(self, request, id):
        user = request.user.has_perm('cobranca.add_cobranca')
        if user == False:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

        data = {}
        today = date.today()
        mes = today.month
        ano = today.year
        if mes > 1 and mes <= 12:
            um_mes_atras = mes - 1
        else:
            um_mes_atras = 12
            um_ano_atras = ano -1
        
        if Cobranca.objects.filter(usuarios__id= id):
            data['messagem_de_error'] = 'Essa cobrança já existe!'
            data['cobranca'] = Cobranca.objects.filter(usuarios__id= id).order_by('-id')
            return render(
                request, 'cobranca.html', data)

        usuario = Usuarios.objects.get(id= id)
        registro_de_dado = registro_de_dados( id, um_mes_atras, um_ano_atras)
        Cobranca.objects.create(
            registros= registro_de_dado,
            valor = usuario.plano.valor,
            mes_referente = date(day=10, month=um_mes_atras, year=ano),
            data_de_vencimento = date(day=10, month=mes, year=ano),
            estado_do_debito = request.POST['estado'],
            link_de_cobranca = request.POST['link'],
            usuarios_id = id,
            )
        data['cobranca'] = Cobranca.objects.filter(usuarios__id= id).order_by('-id')
        return render(
            request, 'cobranca.html', data)

class CobrancaUpdate(LoginRequiredMixin, View):
    def get(self, request, id):
        user = request.user.has_perm('cobranca.change_cobranca')
        if user == False:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
            
        data={}
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
        id = cobranca.usuarios.id
        return redirect('cobranca', id)
    
class Usuario(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user.has_perm('usuarios.view_usuarios')
        if user == False:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

        data={}
        plano = request.GET.get('plano')
          
        data['todos_os_plano'] = Plano.objects.all()
        if plano:
            data['usuario']= Usuarios.objects.filter(plano__nome= plano)
        else:
            data['usuario']= Usuarios.objects.all()
        return render(
            request, 'usuarios.html', data)

