
from django.contrib.auth.models import User
from pessoa.models import Funcionario, Sexo
from usuarios.models import Usuarios, Plano
from django.views import View
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
#from django.contrib.auth.models import Permission
#from django.contrib.contenttypes.models import ContentType
# Create your views here.

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
            permissao= Group.objects.get(name='Administrador') # Buscando permissão
            permissao_add= usuario.groups.add(permissao)# Inserindo permissão de administrador no novo usuário
            cliente = usuario.id # Buscando o ID do usuário criado
            
            plano= Plano.objects.first()
            plano= plano.id
            novo_usuario = Usuarios.objects.create(
                usuario_cliente= cliente, user_id= cliente, plano_id= plano,
                cpf_cnpj= request.POST['cpf_cnpj'],
                nome_fantazia= request.POST['nome_fantazia'])# Criando novo usuário_cliente administrador

            data['usuario'] = usuario
            data['novo_usuario'] = novo_usuario
    
            return redirect('login')

class UpdateUsuario(LoginRequiredMixin, View):
    def get(self, request):
        user_logado = request.user # Obitendo o usuário logado
        user_logado = user_logado.id # obitendo o ID do usuário logado
        usuario = Usuarios.objects.get(user_id = user_logado)

        return render(request,'update-usuario.html', {'usuario': usuario})
    
    def post(self, request):
       
        user_logado = request.user # Obitendo o usuário logado
        user_logado = user_logado.id # obitendo o ID do usuário logado
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

class NovoFuncionario(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user.has_perm('pessoa.add_funcionario')
        if user == False:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

        user_logado = request.user # Obitendo o usuário logado
        user_logado = user_logado.id # obitendo o ID do usuário logado
        if Funcionario.objects.filter(user_id = user_logado): # verificando se o usuário existe em funcionários
            funcionario= Funcionario.objects.get(user__id = user_logado) # buscado funcionário baseado no usuário logado
            #usuarioId= funcionario.usuarios.id # Buscando o ID dousuário administrador com base no usuário logado
            usuarioCliente= funcionario.usuarios.usuario_cliente # Buscando o ID dousuário administrador com base no usuário logado
        else:
            usuario = Usuarios.objects.get(user_id = user_logado) # Buscando usuário administrador com base no usuário logado
            #usuarioId = usuario.id # Obitendo o id  do usuário administrador
            usuarioCliente= usuario.usuario_cliente # Obitendo o id  do usuário_cliente administrador

        usuarios= Funcionario.objects.filter(usuarios__usuario_cliente= usuarioCliente)
        return render(
            request, 'novo-funcionario.html',{'usuarios': usuarios })

    def post(self, request):
        user = request.user.has_perm('pessoa.add_funcionario')
        if user == False:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

        data = {}
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

            permissaos= Group.objects.get(name= request.POST['permissao']) # Buscando permissão
            permissao_add= usuario.groups.add(permissaos)# Inserindo permissão ao novo usuário
            
            usuario= usuario.id # Id do novo usuario local criado
            funcionario = Funcionario.objects.create(
                usuarios_id = usuarioId, user_id= usuario,
                nome= request.POST['primeiro_nome'],
                segundo_nome= request.POST['segundo_nome'],
                )
            
            data['usuario'] = usuario
            data['funcionario'] = funcionario
            data['usuarios']= Funcionario.objects.filter(usuarios__usuario_cliente= usuarioCliente)
            return render(
                request, 'novo-funcionario.html', data)

class UpdateFuncionario(LoginRequiredMixin, View):
    def get(self, request, id):
        user = request.user.has_perm('pessoa.change_funcionario')
        if user == False:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

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

        funcionarios = Funcionario.objects.get(user__id = id)
        usuario_adm = funcionarios.usuarios.usuario_cliente
        if  usuario_adm == usuarioCliente:
            data = {}
            usuario= User.objects.get(id= id)
            data['usuario'] = usuario
            data['permissoes'] = usuario.groups.all()
            data['usuarioCliente'] = usuarioCliente
            return render(
                    request, 'update-funcionario.html', data)
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    def post(self, request, id):
        user = request.user.has_perm('pessoa.change_funcionario')
        if user == False:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

        data = {}
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
        
        usuario= User.objects.get(id= id)
        user_atualizado= request.POST['username']
        user_antigo= usuario.username
        senha= request.POST['password']
        usuario_exit = User.objects.filter(username= user_atualizado)or 0
        funcionarios = Funcionario.objects.get(user__id = id)
        usuario_adm = funcionarios.usuarios.usuario_cliente
        if  usuario_adm == usuarioCliente:
            
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
                permissao= Group.objects.get(name= request.POST['permissao']) # Buscando permissão
                permissao_add= usuario.groups.add(permissao)# Inserindo permissão ao novo usuário
                
            if request.POST['permissao_delete']:   
                permissao= Group.objects.get(name= request.POST['permissao_delete']) # Buscando permissão
                permissao_delete= usuario.groups.remove(permissao)# Excluindo permissão
            
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
        
    funcionarios = Funcionario.objects.get(user__id = id)
    usuario_adm = funcionarios.usuarios.usuario_cliente
    if  usuario_adm == usuarioCliente:
        
        data  = {}
        usuario= User.objects.get(id= id)
        if request.method == 'POST':
            usuario.delete()
            return redirect('novo-funcionario')
        else:
            return render(request, 'delete-funcionario.html',data)
    else:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))