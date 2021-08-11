
from django.contrib.auth.models import User
from pessoa.models import Funcionario
from usuarios.models import Usuarios
from django.views import View
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
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
            novo_usuario = Usuarios.objects.create(
                usuario_cliente= cliente, user_id= cliente, plano_id= '1')# Criando novo usuário_cliente administrador

            data['usuario'] = usuario
            data['novo_usuario'] = novo_usuario
            return render(
                request, 'novo-usuario.html', data)

class NovoFuncionario(View):
    def get(self, request):
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
        data = {}
        data['password'] = request.POST['password']
        data['username'] = request.POST['username']
        data['email'] = request.POST['email']
        data['primeiro_nome']= request.POST['primeiro_nome']
        data['segundo_nome']= request.POST['segundo_nome']
        data['ativo']= request.POST['ativo'],
        data['permissao']= request.POST['permissao']

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

        email = User.objects.filter(email= request.POST['email'])or 0
        if email !=  0:
            data['mensagen_de_erro_email'] = 'E-mail já existe!'
            return render(
                request, 'novo-funcionario.html', data)

        else:
            usuario = User.objects.create_user(
                password= request.POST['password'],
                username= request.POST['username'],
                email= request.POST['email'],
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

class UpdateFuncionario(View):
    def get(self, request, id):
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
       
        data = {}
        usuario= User.objects.get(id= id)
        data['usuario'] = usuario
        data['permissoes'] = usuario.groups.all()
        return render(
                request, 'update-funcionario.html', data)

    def post(self, request, id):
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

        usuario.id = id
        #usuario.password= request.POST['password']
        #usuario.username= request.POST['username']
        usuario.email= request.POST['email']
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
        usuario.save()
        return render(
                request, 'update-funcionario.html', data)

@login_required()
def funcionarioDelete(request, id):
    #user = request.user.has_perm('pessoa.delete_fornecedor')
    #if user == False:
       # return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    data  = {}
    usuario= User.objects.get(id= id)
    if request.method == 'POST':
        usuario.delete()
        return redirect('novo-funcionario')
    else:
        return render(request, 'delete-funcionario.html',data)
