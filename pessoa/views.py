from django.shortcuts import render, redirect
from .models import Fornecedor, Cliente
from django.views import View
#from django.contrib.auth.models import  User
#from django.shortcuts import get_object_or_404
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from usuarios.models import Usuarios
from pessoa.models import Funcionario
#from django.contrib.auth.mixins import PermissionRequiredMixin
#from django.contrib.auth.decorators import permission_required
from django.conf import settings
#from django.urls import reverse_lazy
#from .forms import ProdutoForm

class NovoFornecedor(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user.has_perm('pessoa.add_fornecedor')
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

        fornecedor = Fornecedor.objects.filter(usuarios__usuario_cliente= usuario).order_by('-id')
        busca= request.GET.get('fornecedor',None)
        if busca:
            fornecedor=Fornecedor.objects.filter(usuarios__usuario_cliente= usuario, cnpj__iexact=busca)
        return render(
            request, 'pessoa/novo-fornecedor.html', {'fornecedor': fornecedor})

    def post(self, request):
        user = request.user.has_perm('pessoa.add_fornecedor')
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

        fornecedor = Fornecedor.objects.create(
            nome_fantazia = request.POST['nome_fantazia'],
            cnpj = request.POST['cnpj'],
            data_de_criacao = request.POST['data_de_criacao'] or None,
            nascionalidade = request.POST['nascionalidade'],
            cep = request.POST['cep'],
            rua = request.POST['rua'],
            quadra = request.POST['quadra'],
            numero = request.POST['numero'],
            setor = request.POST['setor'],
            estado = request.POST['estado'],
            cidade = request.POST['cidade'],
            complemento = request.POST['complemento'],
            pais  = request.POST['pais'],
            Celular = request.POST['Celular'],
            Celular2  = request.POST['Celular2'],
            Telefone  = request.POST['Telefone'],
            email = request.POST['email'],
            user = user_logado, usuarios_id = usuarioId
            )
        data['fornecedor'] = fornecedor
        data['fornecedor']  = Fornecedor.objects.filter(usuarios__usuario_cliente= usuarioCliente).order_by('-id') # listar produtos
        return render(
             request, 'pessoa/novo-fornecedor.html',data)

@login_required()
def fornecedor_delete(request, id):
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
       
    
    fornecedor = Fornecedor.objects.get(id= id)
    usuario_adm = fornecedor.usuarios.id
    if usuario_adm == usuarioId: # Verificar autenticidade do usuário
        data  = {}
        fornecedor = Fornecedor.objects.get(id=id)
        if request.method == 'POST':
            fornecedor.delete()
            return redirect('novo-fornecedor')
        else:
            return render(request, 'pessoa/fornecedor-delete-confirme.html',data)
    else:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

class FornecedorUpdate(LoginRequiredMixin, View):
    def get(self, request, id):
        user = request.user.has_perm('pessoa.change_fornecedor')
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
            
        
        fornecedor = Fornecedor.objects.get(id= id)
        usuario_adm = fornecedor.usuarios.id
        if usuario_adm == usuarioId: # Verificar autenticidade do usuário
            return render(
                request, 'pessoa/fornecedor_update.html',{'fornecedor': fornecedor})
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
            
    def post(self, request, id):
        user = request.user.has_perm('pessoa.change_fornecedor')
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
            
        
        fornecedor = Fornecedor.objects.get(id= id)
        usuario_adm = fornecedor.usuarios.id
        if usuario_adm == usuarioId: # Verificar autenticidade do usuário

            fornecedor.id= id
            fornecedor.nome_fantazia = request.POST['nome_fantazia']
            fornecedor.cnpj = request.POST['cnpj']
            fornecedor.data_de_criacao = request.POST['data_de_criacao'] or None
            fornecedor.nascionalidade = request.POST['nascionalidade']
            fornecedor.cep = request.POST['cep']
            fornecedor.rua = request.POST['rua']
            fornecedor.quadra = request.POST['quadra']
            fornecedor.numero = request.POST['numero']
            fornecedor.setor = request.POST['setor']
            fornecedor.estado = request.POST['estado']
            fornecedor.cidade = request.POST['cidade']
            fornecedor.complemento = request.POST['complemento']
            fornecedor.pais  = request.POST['pais']
            fornecedor.Celular = request.POST['Celular']
            fornecedor.Celular2  = request.POST['Celular2']
            fornecedor.Telefone  = request.POST['Telefone']
            fornecedor.email = request.POST['email']
            fornecedor.user = user_logado
            fornecedor.save()
            return redirect('novo-fornecedor')

        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

class NovoCliente(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user.has_perm('pessoa.add_cliente')
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

        user = request.user.has_perm('pessoa.view_caixa')
        cliente = Cliente.objects.filter(usuarios__usuario_cliente= usuario).order_by('-id')
        busca= request.GET.get('client',None)
        if busca:
            cliente=Cliente.objects.filter(usuarios__usuario_cliente= usuario, cpf_cnpj__iexact=busca)
        return render(
            request, 'pessoa/novo-cliente.html', {'cliente': cliente})
        
    def post(self, request):
        user = request.user.has_perm('pessoa.add_cliente')
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

        cliente = Cliente.objects.create(
            nome = request.POST['nome'],
            segundo_nome = request.POST['segundo_nome'],
            cpf_cnpj = request.POST['cpf_cnpj'],
            data_de_nascimento = request.POST['data_de_nascimento'] or None,
            sexo_id = request.POST['sexo_id'],
            nascionalidade = request.POST['nascionalidade'],
            cep = request.POST['cep'],
            rua = request.POST['rua'],
            quadra = request.POST['quadra'],
            numero = request.POST['numero'],
            setor = request.POST['setor'],
            estado = request.POST['estado'],
            cidade = request.POST['cidade'],
            complemento = request.POST['complemento'],
            pais  = request.POST['pais'],
            Celular = request.POST['Celular'],
            Celular2  = request.POST['Celular2'],
            Telefone  = request.POST['Telefone'],
            email = request.POST['email'],
            user = user_logado, usuarios_id = usuarioId
            )
        data['cliente'] = cliente
        data['cliente']  = Cliente.objects.filter(usuarios__usuario_cliente= usuarioCliente).order_by('-id') # listar produtos
        return render(
             request, 'pessoa/novo-cliente.html',data)
@login_required()
def cleinte_delete(request, id):
    user = request.user.has_perm('pessoa.delete_cliente')
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

    cliente = Cliente.objects.get(id= id)
    usuario_adm = cliente.usuarios.id
    if usuario_adm == usuarioId: # Verificar autenticidade do usuário
        data  = {}
        if request.method == 'POST':
            cliente.delete()
            return redirect('novo-cliente')
        else:
            return render(request, 'pessoa/cliente-delete-confirme.html',data)
    else:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

class ClienteUpdate(LoginRequiredMixin, UpdateView):
    def get(self, request, id):
        user = request.user.has_perm('pessoa.change_cliente')
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
           

        cliente = Cliente.objects.get(id= id)
        usuario_adm = cliente.usuarios.id
        if usuario_adm == usuarioId: # Verificar autenticidade do usuário
            cliente = Cliente.objects.get(id= id)
            return render(request, 'pessoa/cliente_update.html',{'cliente': cliente})
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    def post(self, request, id):
        user = request.user.has_perm('pessoa.change_cliente')
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

        cliente = Cliente.objects.get(id= id)
        usuario_adm = cliente.usuarios.id
        if usuario_adm == usuarioId: # Verificar autenticidade do usuário

            cliente.id= id
            cliente.nome = request.POST['nome']
            cliente.segundo_nome = request.POST['segundo_nome']
            cliente.cpf_cnpj = request.POST['cpf_cnpj']
            cliente.data_de_nascimento = request.POST['data_de_nascimento'] or None
            cliente.sexo_id = request.POST['sexo_id']
            cliente.nascionalidade = request.POST['nascionalidade']
            cliente.cep = request.POST['cep']
            cliente.rua = request.POST['rua']
            cliente.quadra = request.POST['quadra']
            cliente.numero = request.POST['numero']
            cliente.setor = request.POST['setor']
            cliente.estado = request.POST['estado']
            cliente.cidade = request.POST['cidade']
            cliente.complemento = request.POST['complemento']
            cliente.pais  = request.POST['pais']
            cliente.Celular = request.POST['Celular']
            cliente.Celular2  = request.POST['Celular2']
            cliente.Telefone  = request.POST['Telefone']
            cliente.email = request.POST['email']
            cliente.user = user_logado
            cliente.save()
            return redirect('novo-cliente')

        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))



