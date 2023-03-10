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
    nome = models.CharField(max_length=50, blank=True)
    user = models.CharField(max_length=100, blank=True, null=True)
    usuarios = models.ForeignKey(Usuarios, null=True, on_delete=models.CASCADE)


    def __str__(self): # METODO CONSTRUTOR
       return self.nome

class Promocao(models.Model):
    descricao = models.CharField(max_length=50,  null = True, verbose_name="Descrição")
    quantidade_promocional = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    desconto = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    data_inicio = models.DateField(blank=True, null=True)
    data_termino = models.DateField(blank=True, null=True)
    user = models.CharField(max_length=100, blank=True, null=True)
    usuarios = models.ForeignKey(Usuarios, null=True, on_delete=models.CASCADE)

    def __str__(self): # METODO CONSTRUTOR
        return str(self.descricao)+ ' , ' + str(self.data_inicio)+ ' Até ' + str(self.data_termino)

class Produto (models.Model):
    nome = models.CharField(max_length=30,  blank=True)
    categoria = models.ForeignKey(
        Categoria, verbose_name='Categoria', on_delete=models.CASCADE, default=1)
    promocao = models.ForeignKey(
        Promocao, null = True, on_delete=models.CASCADE, verbose_name="Promoção")
    codigo = models.CharField(max_length=13, blank=False)
    percentagem_de_lucro = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    valor_venal = models.DecimalField(max_digits=9, decimal_places= 2, default=0)
    valor_compra = models.DecimalField(max_digits=9, decimal_places=2, blank=False, default=0)
    entrada = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    saida = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    estoque = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    data_hora = models.DateTimeField(default=timezone.now)
    imagem = models.ImageField( blank=True)
    user = models.CharField(max_length=100, blank=True, null=True)
    usuarios = models.ForeignKey(Usuarios, null=True, on_delete=models.CASCADE)


    def __str__(self): # METODO CONSTRUTOR
        return str(self.nome)+ ' - ' +str(self.id)

    def atualizar_estoque(self):
        # entrada de mercadoria
        entrada_de_mercadoria = self.entradamercadoria_set.all().aggregate(
           total_entrada = Sum(F('quantidade'), output_Field=DecimalField()))
        total_entrada = entrada_de_mercadoria['total_entrada'] or 0
        self.entrada = total_entrada
        Produto.objects.filter(id=self.id).update(entrada = total_entrada)

        # somando o total de item 
        item_do_pedido = self.itemdopedido_set.all().aggregate(
            total_item = Sum(F('quantidade_de_itens'), output_Field=DecimalField()))
        total_item = item_do_pedido['total_item'] or 0
        self.saida = total_item
        Produto.objects.filter(id=self.id).update(saida = total_item)

        self.estoque= self.entrada - self.saida
        Produto.objects.filter(id=self.id).update(estoque = self.estoque)

        percentagem_de_lucro= float(self.percentagem_de_lucro)
        if percentagem_de_lucro > 0:
            valor_produto= float(
                self.valor_compra) * float(
                    self.percentagem_de_lucro) / 100 + float(self.valor_compra)
            self.valor_venal = valor_produto
            Produto.objects.filter(id=self.id).update(valor_venal = valor_produto)
        if percentagem_de_lucro <= 0:
            lucro= float(self.valor_venal) - float(self.valor_compra)
            lucro_estimado= lucro / float(self.valor_compra) * 100 
            self.percentagem_de_lucro = lucro_estimado
            Produto.objects.filter(id=self.id).update(percentagem_de_lucro = lucro_estimado)

class EntradaMercadoria(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    fornecedor = models.ForeignKey(Fornecedor, null=True, on_delete=models.CASCADE)
    quantidade = models.DecimalField(max_digits=9, decimal_places=2, blank=False, default=1)
    data_hora = models.DateTimeField(default=timezone.now)
    validade_produto = models.DateField(blank=True, null=True)
    user = models.CharField(max_length=100, blank=True, null=True)
    usuarios = models.ForeignKey(Usuarios, null=True, on_delete=models.CASCADE)

    def __str__(self):# METODO CONSTRUTOR
        return str(self.produto.nome)+ ' - ' + str(self.produto.estoque)

@receiver(post_save, sender=Produto)
def update_atualizar_estoque(sender, instance, **kwargs):
    instance.atualizar_estoque()

@receiver(post_save, sender=EntradaMercadoria)
def update_entrada_mercadoria(sender, instance, **kwargs):
    instance.produto.atualizar_estoque()
