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
        pass
    def post(self, request):
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
            data_de_criacao = request.POST['data_de_criacao'],
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
            user_id = user_logado, usuarios_id = usuarioId
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

    data  = {}
    fornecedor = Fornecedor.objects.get(id=id)
    if request.method == 'POST':
        fornecedor.delete()
        return redirect('novo-fornecedor')
    else:
        return render(request, 'pessoa/fornecedor-delete-confirme.html',data)

class FornecedorUpdate(LoginRequiredMixin, UpdateView):
    #permission_required = 'pessoa.change_fornecedor'
    model = Fornecedor
    fields = ['nome_fantazia','cnpj','data_de_criacao','nascionalidade',
        'cep','rua','quadra','numero','setor','estado',
        'cidade','complemento','pais','Celular','Celular2',
        'Telefone','email']
    success_url = '/pessoa/novo-fornecedor/'

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
        pass
    def post(self, request):
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
            data_de_nascimento = request.POST['data_de_nascimento'],
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
            user_id = user_logado, usuarios_id = usuarioId
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

    data  = {}
    cliente = Cliente.objects.get(id=id)
    if request.method == 'POST':
        cliente.delete()
        return redirect('novo-cliente')
    else:
        return render(request, 'pessoa/cliente-delete-confirme.html',data)

class ClienteUpdate(LoginRequiredMixin, UpdateView):
    model = Cliente
    fields = ['nome','segundo_nome','cpf_cnpj','data_de_nascimento','sexo','nascionalidade','cep','rua','quadra','numero','setor','estado','cidade','complemento','pais','Celular','Celular2','Telefone','email']
    success_url = '/pessoa/novo-cliente/'




