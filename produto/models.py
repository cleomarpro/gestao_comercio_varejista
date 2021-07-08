from django.db import models
from django.utils import timezone
#from django.contrib.auth.models import User
from django.db.models import  F,Sum,DecimalField # Max ExpressionWrapper FloatField DecimalField Sum
from django.db.models.signals import post_save
from django.dispatch import receiver
#from django.core.urlresolvers import reverse
#import matplotlib.pyplot as plt
#from vendas.models import ItemDoPedido
#from django.contrib.auth.models import User
from pessoa.models import Fornecedor
from django.contrib.auth.models import User
from usuarios.models import Usuarios
#from datetime import tade
#import math

class Categoria (models.Model):
    nome = models.CharField(max_length=50,blank=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    usuarios = models.ForeignKey(Usuarios, null=True, on_delete=models.CASCADE)


    def __str__(self): # METODO CONSTRUTOR
       return self.nome

class Promocao(models.Model):
    descricao = models.CharField(max_length=50,  null = True, verbose_name="Descrição")
    quantidade_promocional = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    desconto = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    data_inicio = models.DateField(max_length=30,  null= True, blank=True)
    data_termino = models.DateField(max_length=30, null= True, blank=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    usuarios = models.ForeignKey(Usuarios, null=True, on_delete=models.CASCADE)

    def __str__(self): # METODO CONSTRUTOR
        return str(self.descricao)+ ' , ' + str(self.data_inicio)+ ' Até ' + str(self.data_termino)

class Produto (models.Model):
    nome = models.CharField(max_length=30,  blank=True)
    categoria = models.ForeignKey(Categoria, verbose_name='Categoria', on_delete=models.CASCADE, default=1)
    promocao = models.ForeignKey(Promocao, null = True, on_delete=models.CASCADE, verbose_name="Promoção")
    codigo = models.CharField(max_length=13, blank=False)
    percentagem_de_lucro = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    valor_venal = models.DecimalField(max_digits=9, decimal_places= 2, default=0)
    valor_compra = models.DecimalField(max_digits=9, decimal_places=2, blank=False, default=0)
    entrada = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    saida = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    estoque = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    data_hora = models.DateTimeField(default=timezone.now)
    imagem = models.ImageField( blank=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    usuarios = models.ForeignKey(Usuarios, null=True, on_delete=models.CASCADE)


    def __str__(self): # METODO CONSTRUTOR
        return str(self.nome)+ ' - ' +str(self.id)

    def etoque_total(self):
        total = self.entradamercadoria_set.all().aggregate(
           total_entrada = Sum(F('quantidade'), output_Field=DecimalField()))
        entrada_atual = total['total_entrada'] or 0
        self.entrada = entrada_atual
        Produto.objects.filter(id=self.id).update(entrada = entrada_atual)


        total1 = self.itemdopedido_set.all().aggregate(
            total_saida = Sum(F('quantidade_de_itens'), output_Field=DecimalField()))
        saida_atual = total1['total_saida'] or 0
        self.saida = saida_atual
        Produto.objects.filter(id=self.id).update(saida = saida_atual)

        total2 = self.entrada - self.saida
        self.estoque= total2
        Produto.objects.filter(id=self.id).update(estoque = total2)

        valor_produto= float(self.valor_compra) * float(self.percentagem_de_lucro) / 100 + float(self.valor_compra)
        self.valor_venal = valor_produto
        Produto.objects.filter(id=self.id).update(valor_venal = valor_produto)

class EntradaMercadoria(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE, blank=True)
    quantidade = models.DecimalField(max_digits=9, decimal_places=2, blank=False, default=1)
    data_hora = models.DateTimeField(default=timezone.now)
    validade_produto = models.DateField(max_length=30, null= True, blank=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    usuarios = models.ForeignKey(Usuarios, null=True, on_delete=models.CASCADE)


    def __str__(self):# METODO CONSTRUTOR
        return str(self.produto.nome)+ ' - ' + str(self.produto.estoque)

@receiver(post_save, sender=Produto)
def update_total_estoque(sender, instance, **kwargs):
    instance.etoque_total()

@receiver(post_save, sender=EntradaMercadoria)
def update_total_entrada(sender, instance, **kwargs):
    instance.produto.etoque_total()
'''
def total_estoque_saida(self):
tot = self.itemdopedido_set.all().aggregate(
total_esto=Sum(F('quantidade') - F('produto__estoque'), output_field=DecimalField()))
['total_esto'] or 0
self.estoque = tot
Produto.objects.filter(id=self.id).update(estoque = tot)

@receiver(post_save, sender=ItemDoPedido)
def update_total_estoque_saida(sender, instance, **kwargs):
instance.produto.total_estoque_saida()
'''

'''
python manage.py makemigrations (comando para migrar para o django)
python manage.py migrate
(comanto para moigra para o banco)
source venvgestao/bin/activate (ativar a venv)
python -m pip install Pillow (campo de iamgem ou  arquivo)

mensalista = models.ForeignKey(Mensalista, on_delete=models.CASCADE)
detalhe = models.TextField()
email = models.EmailField()
pago= models.BooleanField(default=False)
'''

