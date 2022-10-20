from django.shortcuts import render , redirect
from .models import Produto, Categoria, EntradaMercadoria , Fornecedor, Promocao, SaidaMercadoria
#from fluxo_de_caixa.models import ItemDoPedido
#from django.contrib.auth.models import Permission, User
#from django.contrib.contenttypes.models import ContentType
#from django.shortcuts import get_object_or_404
#from django.http import HttpResponse
from django.views import View
from datetime import date, timedelta
from django.db.models import Q
#from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.conf import settings
#from django.contrib.auth.models import User
from usuarios.models import Usuarios
from pessoa.models import Funcionario
#from django.urls import reverse_lazy
#from .forms import ProdutoForm

class NovoProduto(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user.has_perm('produto.add_produto')
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
        produto=Produto.objects.filter(usuarios__usuario_cliente= usuario).order_by('-id')
        categoria = Categoria.objects.filter(usuarios__usuario_cliente= usuario).order_by('-id')
        promocao = Promocao.objects.filter(usuarios__usuario_cliente= usuario).order_by('-id')
        return render(request, 'produto/produto.html', {
            'categoria': categoria, 'produto': produto,
            'today': today, 'promocao':promocao
            })
     
    def post(self, request): 
        data = {}
        today = date.today()
        #data['imagem'] = request.POST['imagem']

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

        produto= Produto.objects.filter(usuarios__usuario_cliente= usuarioCliente, codigo= request.POST['codigo']) or 0
        if produto != 0:
            data['mensagen_de_erro'] = 'Esse produto já existe!'
            data['produto']  = Produto.objects.filter(usuarios__usuario_cliente= usuarioCliente) # listar produtos recem cadastrados
            data['categoria'] =Categoria.objects.filter(usuarios__usuario_cliente= usuarioCliente).order_by('-id')
            data['promocao'] = Promocao.objects.filter(usuarios__usuario_cliente= usuarioCliente).order_by('-id')
            return render(
                request, 'produto/produto.html', data)
        else:
            produto = Produto.objects.create(
                nome = request.POST['nome'],
                categoria_id = request.POST['categoria_id'],
                codigo = request.POST['codigo'],
                percentagem_de_lucro = request.POST['percentagem_de_lucro'].replace(',', '.') or 0,
                valor_venal = request.POST['valor_venal'].replace('.','').replace(',','.').replace('R$\xa0','').replace('R$','') or 0,
                promocao_id = request.POST['promocao' ],
                valor_compra = request.POST['valor_compra'].replace('.','').replace(',','.').replace('R$\xa0','').replace('R$',''),
                user = user_logado, usuarios_id = usuarioId
                #imagem = request.POST['imagem'],
                )

            #data['form_produto'] = produtoForm()
            data['produto'] = produto
            data['produto']  = Produto.objects.filter(usuarios__usuario_cliente= usuarioCliente).order_by('-id') # listar produtos recem cadastrados
            data['categoria'] =Categoria.objects.filter(usuarios__usuario_cliente= usuarioCliente).order_by('-id')
            data['promocao'] = Promocao.objects.filter(usuarios__usuario_cliente= usuarioCliente).order_by('-id')
            data['today'] = today
            return render(
                request, 'produto/produto.html', data)

@login_required()
def produto_delete(request, id):
    user = request.user.has_perm('produto.delete_produto')
    if user == False:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    data  = {}
    user_logado = request.user # Obitendo o usuário logado
    user_logado = user_logado.id # obitendo o ID do usuário logado
    if Funcionario.objects.filter(user_id = user_logado): # verificando se o usuário existe em funcionários
        funcionario= Funcionario.objects.get(user__id = user_logado) # buscado funcionário baseado no usuário logado
        usuario= funcionario.usuarios.id # Buscando o ID dousuário administrador com base no usuário logado
    else:
        usuario = Usuarios.objects.get(user_id = user_logado) # Buscando usuário administrador com base no usuário logado
        usuario = usuario.id # Obitendo o id  do usuário administrador
    
    produto = Produto.objects.get(id=id)
    usuario_adm= produto.usuarios.id
    if usuario_adm == usuario: # Verificar autenticidade do usuário
        if request.method == 'POST':
            produto.delete()
            return redirect('produto')
        else:
            return render(request, 'produto/delete-produto-confirm.html',data)
    else:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
class ProdutoUpdate(LoginRequiredMixin, View):
    def get(self, request, id):
        data = {}
        user = request.user.has_perm('produto.add_produto')
        if user == False:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
            
        else:
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
           
            produto = Produto.objects.get(id=id)
            usuario_adm= produto.usuarios.id
            if usuario_adm == usuarioId: # Verificar autenticidade do usuário

                data['produto']  = Produto.objects.get(id= id)
                data['categoria'] =Categoria.objects.filter(usuarios__usuario_cliente= usuarioCliente).order_by('-id')
                data['promocao'] = Promocao.objects.filter(usuarios__usuario_cliente= usuarioCliente).order_by('-id')
                return render(request, 'produto/produto_update.html',data)
            else:
                return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

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
        
        produto = Produto.objects.get(id=id)
        usuario_adm= produto.usuarios.id
       
        codigo_produto_autal= produto.codigo
        novo_codigo_produto= request.POST['codigo']
        produto_id= Produto.objects.filter(usuarios__usuario_cliente= usuarioCliente, codigo= request.POST['codigo']) or 0
        if codigo_produto_autal != novo_codigo_produto: # verifica se o código do produto foi alterado ous se já existe
         
            if produto_id != 0:
                data['mensagen_de_erro'] = 'Esse produto já existe!'
                data['produto']  = Produto.objects.filter(usuarios__usuario_cliente= usuarioCliente) # listar produtos recem cadastrados
                data['categoria'] =Categoria.objects.filter(usuarios__usuario_cliente= usuarioCliente).order_by('-id')
                data['promocao'] = Promocao.objects.filter(usuarios__usuario_cliente= usuarioCliente).order_by('-id')
                return render(
                    request, 'produto/produto_update.html', data)
        if usuario_adm == usuarioId: # Verificar autenticidade do usuário
            produto.id = id
            produto.nome = request.POST['nome']
            produto.categoria_id = request.POST['categoria_id']
            produto.codigo = request.POST['codigo']
            if request.POST['percentagem_de_lucro']:
                produto.percentagem_de_lucro = request.POST['percentagem_de_lucro'].replace(',', '.')
            produto.valor_venal = request.POST['valor_venal'].replace('.','').replace(',','.').replace('R$\xa0','').replace('R$','') or 0
            produto.promocao_id = request.POST['promocao' ]
            produto.valor_compra = request.POST['valor_compra'].replace('.','').replace(',','.').replace('R$\xa0','').replace('R$','')
            produto.user = user_logado
            #imagem = request.POST['imagem'],
            produto.save()
            return redirect('produto')

        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

class ListaProdutos(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user.has_perm('produto.view_produto')
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

        produto=Produto.objects.filter(usuarios__usuario_cliente= usuario).order_by('-id')
        produt= request.GET.get('produt',None)
        if produt:
            produto=Produto.objects.filter(codigo__icontains=produt, usuarios__usuario_cliente= usuario) # trocar o 'iexact ' por 'icontains' para digitar do objeto completo
        return render(request, 'produto/listar-produto.html', {'produto': produto})

class FiltroPorCategoria(LoginRequiredMixin, View): 
    def get(self, request):

        user_logado = request.user # Obitendo o usuário logado
        user_logado = user_logado.id # obitendo o ID do usuário logado
        if Funcionario.objects.filter(user_id = user_logado): # verificando se o usuário existe em funcionários
            funcionario= Funcionario.objects.get(user__id = user_logado) # buscado funcionário baseado no usuário logado
            usuario= funcionario.usuarios.usuario_cliente # Buscando o ID dousuário administrador com base no usuário logado
        else:
            usuario = Usuarios.objects.get(user_id = user_logado) # Buscando usuário administrador com base no usuário logado
            usuario = usuario.usuario_cliente # Obitendo o id  do usuário administrador

        categoria = Categoria.objects.filter(usuarios__usuario_cliente= usuario).order_by('-id')
        produto = Produto.objects.filter(usuarios__usuario_cliente= usuario).order_by
        busca= request.GET.get('produt',None)
        busca_categoria= request.GET.get('busca_categoria',None)
        if busca:
            produto=Produto.objects.filter(codigo__iexact=busca, usuarios__usuario_cliente= usuario) # trocar o 'iexact ' por 'icontains' para digitar do objeto completo
        if busca_categoria:
            produto = Produto.objects.filter(categoria__id= busca_categoria, usuarios__usuario_cliente= usuario).order_by('-id') # listar produtos recem cadastrados
        return render(
            request, 'produto/produto.html', {
                'produto': produto, 'categoria': categoria
                })

class NovaPromocao (LoginRequiredMixin, View):
    def get(self, request):
        user = request.user.has_perm('produto.add_promocao')
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

        #produto=Produto.objects.filter(usuarios__usuario_cliente= usuario).order_by('-id')
        categoria = Categoria.objects.filter(usuarios__usuario_cliente= usuario).order_by('-id')
        promocao = Promocao.objects.filter(usuarios__usuario_cliente= usuario).order_by('-id')
        return render(
            request, 'produto/promocao.html', {
                'promocao': promocao, 'categoria': categoria
                })
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

        promocao = Promocao.objects.create(
            quantidade_promocional = request.POST['quantidade_promocional'].replace(',', '.'),
            desconto = request.POST['desconto'].replace(',', '.'),
            data_inicio = request.POST['data_inicio'] ,
            data_termino = request.POST['data_termino' ],
            descricao = request.POST['descricao' ],
            user = user_logado, usuarios_id = usuarioId
            )
        data['prom'] = promocao
        data['promocao']  = Promocao.objects.filter(usuarios__usuario_cliente= usuarioCliente).order_by('-id')
        return render(
            request, 'produto/promocao.html', data)

class PromocaoUpdate (LoginRequiredMixin, View):
    def get(self, request, id):
        user = request.user.has_perm('produto.add_promocao')
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
            
        promocao = Promocao.objects.get(id= id)
        usuario_adm= promocao.usuarios.id
        if usuario_adm == usuarioId: # Verificar autenticidade do usuário
            return render(
                request, 'produto/promocao-update.html',{'promocao': promocao})
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))


    def post(self, request, id):
        data = {}
        user = request.user.has_perm('produto.add_promocao')
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

        promocao = Promocao.objects.get(id= id)
        usuario_adm= promocao.usuarios.id
        if usuario_adm == usuarioId: # Verificar autenticidade do usuário

            promocao = Promocao.objects.get(id= id)
            promocao.id= id
            promocao.quantidade_promocional = request.POST['quantidade_promocional'].replace(',', '.')
            promocao.desconto = request.POST['desconto'].replace(',', '.')
            promocao.data_inicio = request.POST['data_inicio'] 
            promocao.data_termino = request.POST['data_termino' ]
            promocao.descricao = request.POST['descricao' ]
            promocao.user = user_logado
            promocao.save()
            return redirect('promocao')
     
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

def promocao_delete(request, id):
    user = request.user.has_perm('produto.delete_promocao')
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
        

    data  = {}

    promocao = Promocao.objects.get(id=id)
    usuario_adm= promocao.usuarios.id
    if usuario_adm == usuarioId: # Verificar autenticidade do usuário
        if request.method == 'POST':
            promocao.delete()
            return redirect('promocao')
        else:
            return render(request, 'produto/delete-promocao-confirm.html',data)
    else:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

class Categoria_de_produto (LoginRequiredMixin, View):
    def get(self, request):
        user = request.user.has_perm('produto.add_categoria')
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

        categoria = Categoria.objects.filter(usuarios__usuario_cliente= usuario).order_by('-id')
        return render(
            request, 'produto/categoria.html', {'categoria': categoria})
        
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

        categoria = Categoria.objects.create(
            nome = request.POST['nome'],
            user = user_logado, usuarios_id = usuarioId
            )
        data['categoria'] = categoria
        data['categoria']  = Categoria.objects.filter(usuarios__usuario_cliente= usuarioCliente).order_by('-id') # listar produtos
        return render(
            request, 'produto/categoria.html', data)

class CategoriaUpdate(LoginRequiredMixin, View):
    def get(self, request, id):
        user = request.user.has_perm('produto.add_categoria')
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
           

        categoria = Categoria.objects.get(id=id)
        usuario_adm= categoria.usuarios.id
        if usuario_adm == usuarioId: # Verificar autenticidade do usuário
            return render(
                request, 'produto/categoria_update.html', {'categoria': categoria})
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
      
    def post(self, request, id):
        user = request.user.has_perm('produto.change_categoria')
        if user == False:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

        data = {}
        user_logado = request.user # Obitendo o usuário logado
        user_logado = user_logado.id # obitendo o ID do usuário logado
        if Funcionario.objects.filter(user_id = user_logado): # verificando se o usuário existe em funcionários
            funcionario= Funcionario.objects.get(user__id = user_logado) # buscado funcionário baseado no usuário logado
            usuarioId= funcionario.usuarios.id # Buscando o ID dousuário administrador com base no usuário logado
            
        else:
            usuario = Usuarios.objects.get(user_id = user_logado) # Buscando usuário administrador com base no usuário logado
            usuarioId = usuario.id # Obitendo o id  do usuário administrador

        categoria = Categoria.objects.get(id=id)
        usuario_adm= categoria.usuarios.id
        if usuario_adm == usuarioId: # Verificar autenticidade do usuário 

            categoria = Categoria.objects.get(id=id)
            categoria.id= id
            categoria.nome = request.POST['nome']
            categoria.user = user_logado
            categoria.save()
            return redirect('categoria') 

        else:
             return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

def categoria_delete(request, id):
    user = request.user.has_perm('produto.delete_categoria')
    if user == False:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    data  = {}
    user_logado = request.user # Obitendo o usuário logado
    user_logado = user_logado.id # obitendo o ID do usuário logado
    if Funcionario.objects.filter(user_id = user_logado): # verificando se o usuário existe em funcionários
        funcionario= Funcionario.objects.get(user__id = user_logado) # buscado funcionário baseado no usuário logado
        usuarioId= funcionario.usuarios.id # Buscando o ID dousuário administrador com base no usuário logado

    else:
        usuario = Usuarios.objects.get(user_id = user_logado) # Buscando usuário administrador com base no usuário logado
        usuarioId = usuario.id # Obitendo o id  do usuário administrador
       
    categoria = Categoria.objects.get(id=id)
    usuario_adm= categoria.usuarios.id
    if usuario_adm == usuarioId: # Verificar autenticidade do usuário 
        if request.method == 'POST':
            categoria.delete()
            return redirect('categoria')
        else:
            return render(request, 'produto/delete-categoria-confirm.html',data)
    else:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

class Entrada_Mercadoria (LoginRequiredMixin, View):
    def get(self, request):
        user = request.user.has_perm('produto.add_entradamercadoria')
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
        mes_atual = today.month
        fornecedor= Fornecedor.objects.filter(usuarios__usuario_cliente= usuario).order_by('-id')
        entrada_Mercadoria = EntradaMercadoria.objects.filter(
            usuarios__usuario_cliente= usuario, data_hora__month = mes_atual).order_by('-id')
        produto = Produto.objects.filter(usuarios__usuario_cliente= usuario).order_by('-id')
        
        return render(
            request, 'produto/entrada-mercadoria.html', {
                'produto': produto, 'fornecedor': fornecedor,
                'entrada_Mercadoria': entrada_Mercadoria
                })
    def post(self, request):
        today = date.today()
        mes_atual = today.month
        data = {}
        data['produto'] = request.POST['produto']
        data['fornecedor'] = request.POST['fornecedor']
        data['quantidade'] = request.POST['quantidade']
        data['validade_produto'] = request.POST['validade_produto']

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
    
        entrada_Mercadoria = EntradaMercadoria.objects.create(
            produto_id = request.POST['produto'],
            fornecedor_id= request.POST['fornecedor'],
            quantidade = request.POST['quantidade'].replace(',', '.'),
            validade_produto= request.POST['validade_produto'] or '2000-02-03',
            user = user_logado, usuarios_id = usuarioId
            )
        data['entrada_Mercadoria']=entrada_Mercadoria
        data['entrada_Mercadoria']=EntradaMercadoria.objects.filter(
            usuarios__usuario_cliente= usuarioCliente, data_hora__month = mes_atual).order_by('-id')
        data['produto']  = Produto.objects.filter(usuarios__usuario_cliente= usuarioCliente).order_by('-id')
        data['fornecedor']  = Fornecedor.objects.filter(usuarios__usuario_cliente= usuarioCliente).order_by('-id')
        return render(
            request, 'produto/entrada-mercadoria.html', data)

class EntradaMercadoriaUpdate(LoginRequiredMixin, View):
    def get(self, request, id):
        user = request.user.has_perm('produto.add_entradamercadoria')
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
           
        entrada_Mercadoria= EntradaMercadoria.objects.get(id= id)
        usuario_adm= entrada_Mercadoria.usuarios.id
        if usuario_adm == usuarioId: # Verificar autenticidade do usuário

            entrada_Mercadoria= EntradaMercadoria.objects.get(id= id)
            return render(
                request, 'produto/entrada_mercadoria_update.html',{'entrada_Mercadoria': entrada_Mercadoria})
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    def post(self, request, id):
        user = request.user.has_perm('produto.add_entradamercadoria')
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
            
        entrada_Mercadoria= EntradaMercadoria.objects.get(id= id)
        usuario_adm= entrada_Mercadoria.usuarios.id
        if usuario_adm == usuarioId: # Verificar autenticidade do usuário

            entrada_Mercadoria.id= id
            entrada_Mercadoria.produto_id = request.POST['produto']
            if request.POST['fornecedor']:
                entrada_Mercadoria.fornecedor_id= request.POST['fornecedor']
            entrada_Mercadoria.quantidade = request.POST['quantidade'].replace(',', '.')
            if request.POST['validade_produto']:
                entrada_Mercadoria.validade_produto= request.POST['validade_produto']
            entrada_Mercadoria.user_ = user_logado 
            entrada_Mercadoria.save()
            return redirect('entrada-mercadoria')

        else:
             return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

def entradaMercadoria_delete(request, id):
    user = request.user.has_perm('produto.delete_entradamercadoria')
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
       
    entrada_Mercadoria= EntradaMercadoria.objects.get(id= id)
    usuario_adm= entrada_Mercadoria.usuarios.id
    if usuario_adm == usuarioId: # Verificar autenticidade do usuário
        data  = {}
        entrada_Mercadoria = EntradaMercadoria.objects.get(id=id)
        if request.method == 'POST':
            entrada_Mercadoria.delete()
            return redirect('entrada-mercadoria')
        else:
            return render(request, 'produto/entradaMercadoria-delete-confirme.html',data)
    else:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

class SaidaDeMercadoria(LoginRequiredMixin, View):
    def get(self, request):
        data={}
        user = request.user.has_perm('produto.add_entradamercadoria')
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
        mes_atual = today.month
        fornecedor= Fornecedor.objects.filter(usuarios__usuario_cliente= usuario).order_by('-id')
        data["saida_mercadoria"] = SaidaMercadoria.objects.filter(
            usuarios__usuario_cliente= usuario, data_hora__month = mes_atual).order_by('-id')
        data['produto'] = Produto.objects.filter(usuarios__usuario_cliente= usuario).order_by('-id')
        return render(
            request, 'produto/saida_mercadoria.html', data)
     
    def post(self, request):
        today = date.today()
        mes_atual = today.month
        data = {}
        data['produto'] = request.POST['produto']
        data['quantidade'] = request.POST['quantidade']
        data['validade_produto'] = request.POST['estoque_fisico_atual']

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
    
        saida_mercadoria = SaidaMercadoria.objects.create(
            produto_id = request.POST['produto'],
            quantidade = request.POST['quantidade'].replace(',', '.'),
            estoque_fisico_atual= request.POST['estoque_fisico_atual'].replace(',', '.'),
            user = user_logado, usuarios_id = usuarioId
            )
        #data['entrada_Mercadoria']=saida_mercadoria
        data['saida_mercadoria']=SaidaMercadoria.objects.filter(
            usuarios__usuario_cliente= usuarioCliente, data_hora__month = mes_atual).order_by('-id')
        data['produto']  = Produto.objects.filter(usuarios__usuario_cliente= usuarioCliente).order_by('-id')
        data['fornecedor']  = Fornecedor.objects.filter(usuarios__usuario_cliente= usuarioCliente).order_by('-id')
        return render(
            request, 'produto/saida_mercadoria.html', data)

class FiltrarEntadaPorCategoria(LoginRequiredMixin, View):
    def get(self, request):

        user_logado = request.user # Obitendo o usuário logado
        user_logado = user_logado.id # obitendo o ID do usuário logado
        if Funcionario.objects.filter(user_id = user_logado): # verificando se o usuário existe em funcionários
            funcionario= Funcionario.objects.get(user__id = user_logado) # buscado funcionário baseado no usuário logado
            usuario= funcionario.usuarios.usuario_cliente # Buscando o ID dousuário administrador com base no usuário logado
        else:
            usuario = Usuarios.objects.get(user_id = user_logado) # Buscando usuário administrador com base no usuário logado
            usuario = usuario.usuario_cliente # Obitendo o id  do usuário administrador

        today = date.today()
        mes_atual = today.month
        produto = Produto.objects.filter(usuarios__usuario_cliente= usuario).order_by('-id')
        fornecedor= Fornecedor.objects.filter(usuarios__usuario_cliente= usuario).order_by('-id')
        entrada_Mercadoria = EntradaMercadoria.objects.filter(
            usuarios__usuario_cliente= usuario, data_hora__month = mes_atual ).order_by('-id')
        Mes= request.GET.get('mes',None)
        Ano= request.GET.get('ano',None)
        busca= request.GET.get('produt',None)
        if busca:
            entrada_Mercadoria = EntradaMercadoria.objects.filter(
                usuarios__usuario_cliente= usuario, produto__id= busca).order_by('-id')
        if Mes and Ano:
            entrada_Mercadoria = EntradaMercadoria.objects.filter(
                usuarios__usuario_cliente= usuario, data_hora__year= Ano, data_hora__month= Mes).order_by('-id')
        return render(
            request, 'produto/entrada-mercadoria.html', {
                'entrada_Mercadoria': entrada_Mercadoria,
                'produto': produto, 'fornecedor': fornecedor
                })

class ValidadeProdutos (LoginRequiredMixin, View):
    def get(self, request):
        user = request.user.has_perm('produto.view_produto')
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
        ultimos_dias = today - timedelta(days= 10)
        proximo_dias = today + timedelta(days= 10)
        produto_a_vencer = EntradaMercadoria.objects.filter(
            ~Q(produto__estoque = 0 ), Q(validade_produto__range = (ultimos_dias, proximo_dias)), usuarios__usuario_cliente= usuario).order_by('validade_produto')

        DIA = request.GET.get('dia',None)
        DIA2 = request.GET.get('dia2',None)

        if DIA and DIA2 :
            produto_a_vencer = EntradaMercadoria.objects.filter(
                usuarios__usuario_cliente= usuario, validade_produto__range= (DIA, DIA2)).order_by('validade_produto')
        return render(
            request, 'produto/validade-produtos.html', {
                'produto_a_vencer': produto_a_vencer,
                'today': today
                })





