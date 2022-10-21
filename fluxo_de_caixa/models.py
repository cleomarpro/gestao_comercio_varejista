from django.db import models
from django.utils import timezone
from django.db.models import Sum, F, FloatField
from django.db.models.signals import post_save
from django.dispatch import receiver
from produto.models import Produto
from django.contrib.auth.models import User
from usuarios.models import Cobranca, Usuarios
from pessoa.models import Funcionario
from datetime import date
#import datetime

class Caixa(models.Model):
    nome_do_caixa = models.CharField(max_length=30)
    funcionario = models.ForeignKey(Funcionario, null=True, on_delete=models.CASCADE)
    valor_atualizado = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True, default=0)
    user = models.CharField(max_length=100, blank=True, null=True)
    usuarios = models.ForeignKey(Usuarios, null=True, on_delete=models.CASCADE)

    def caixa(self):

#buscando o valor do depósuto
        depositar= self.depositar_sacar_set.all().aggregate(deposito=Sum('depositar'))
        total_do_deposito=depositar['deposito'] or 0

#buscando o valor do saque
        sacar= self.depositar_sacar_set.all().aggregate(saque =Sum('sacar'))
        total_do_saque = sacar['saque'] or 0

# calculo do saldo atual do caixa
        valor_atualizado = float(total_do_deposito) - float(total_do_saque)
        self.valor_atualizado = valor_atualizado
        Caixa.objects.filter(id=self.id).update(valor_atualizado = valor_atualizado)


    def __str__(self):
        return str(self.nome_do_caixa)+ ' - ' + str(self.funcionario)

class Depositar_sacar(models.Model):
    descricao = models.CharField(max_length=100, null=True, blank=True, verbose_name="Descrição")
    estadoDoCaixa = models.CharField(max_length=10, null=True, blank=True, verbose_name="Descrição")
    depositar = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True, default=0)
    venda_realizadas= models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True, default=0)
    saldo_em_caixa = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True, default=0)
    sacar = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True, default=0)
    caixa = models.ForeignKey(Caixa, null=True, on_delete=models.CASCADE)
    data_hora = models.DateTimeField(default=timezone.now)
    user = models.CharField(max_length=100, blank=True, null=True)
    usuarios = models.ForeignKey(Usuarios, null=True, on_delete=models.CASCADE)


    def __str__(self):
        return str(self.sacar)+ ' - ' + str(self.depositar)

class Tipo_de_pagamento(models.Model):
    nome = models.CharField(max_length=30)

    def __str__(self):
        return str(self.nome)

class Venda(models.Model):
    valor = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True, default=0)
    valor_com_desconto = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True, default=0)
    desconto = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True, default=0)
    total_desconto = models.DecimalField(max_digits=9, null=True, blank=True, decimal_places=2, default=0)
    valor_recebido = models.DecimalField(max_digits=9,null=True, blank=True, decimal_places=2, default=0)
    valor_credito = models.FloatField(null=True, blank=True, default=0)
    valor_cedula = models.FloatField(null=True, blank=True, default=0)
    valor_debito = models.FloatField( null=True, blank=True, default=0)
    troco = models.DecimalField(max_digits=9, null=True, blank=True,decimal_places=2, default=0)
    tipo_de_pagamento = models.ForeignKey(Tipo_de_pagamento, null=True, on_delete=models.CASCADE)
    descricao = models.CharField(max_length=100, blank=True)
    finalizada = models.CharField(max_length=20, blank=True, null=True)
    nfe_emitida = models.BooleanField(default=False)
    data_hora = models.DateTimeField(default=timezone.now)
    user = models.CharField(max_length=100, blank=True, null=True)
    user_2 =models.CharField(max_length=1000, blank=True, null=True)
    usuarios = models.ForeignKey(Usuarios, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.descricao) + ' - Cliente: ' + str(self.id) + ' - Valor: ' + str(self.valor)

# calculo do valor total da venda
    def calcular_total(self):
        valor_da_venda = self.itemdopedido_set.all().aggregate(
        valor=Sum((F('quantidade_de_itens') * F('produto__valor_venal')), output_field=FloatField()))
        total_produto=valor_da_venda['valor'] or 0
        self.valor = total_produto
        Venda.objects.filter(id=self.id).update(valor = total_produto)

# calculo de desconto por item
        desconto_item = self.itemdopedido_set.aggregate(
        total_item=Sum(F('quantidade_de_itens') * F('produto__valor_venal') * F('desconto')/100, output_field=FloatField()))
        desconto_por_item= desconto_item['total_item']or 0

# calculo descont da promoçao

        promocao = self.itemdopedido_set.values_list(
            'produto__id','produto__promocao__quantidade_promocional',
            'produto__valor_venal','produto__promocao__desconto',
            'produto__promocao__data_inicio', 'produto__promocao__data_termino'
            ).annotate(d=Sum('quantidade_de_itens'))

        today = date.today()
        total_promocao = 0
        total_da_venda = 0
        if promocao:
            for valor in promocao:
                if valor[4] != None and  valor[5] != None and  valor[1] != None and\
                    valor[6] >= valor[1] and valor[4] and\
                        today >=  valor[4] and today <= valor[5]:

                    calculo_promocao = float(
                        (valor[6] *  valor[2]) * valor[3] /100 or 0)

                    total_promocao +=  calculo_promocao

        total_da_venda = total_produto - desconto_por_item - total_promocao
# calculo do desconto da venda e do total da venda
        desconto_por_venda = total_da_venda * float(self.desconto)/ 100 #desconto por venda
        total_da_venda = total_da_venda - desconto_por_venda
        self.valor_com_desconto = total_da_venda
        Venda.objects.filter(id=self.id).update(valor_com_desconto=total_da_venda)

# Pagamento em crédito
        credito = self.itemdopedido_set.filter(venda__tipo_de_pagamento__id=2)

        if credito:
            self.valor_credito = total_da_venda
            Venda.objects.filter(id=self.id).update(valor_credito = total_da_venda)

#Pagamento em débito
        debito = self.itemdopedido_set.filter(venda__tipo_de_pagamento__id=3)
        if debito:
            self.valor_debito = total_da_venda
            Venda.objects.filter(id=self.id).update(valor_debito = total_da_venda)

# calculo do troco
        total_troco = 0
        if  self.valor_recebido or self.valor_debito or self.valor_credito > 0:
            total_troco = float(self.valor_recebido) + float(self.valor_debito) + float(self.valor_credito) - total_da_venda
            self.troco = float(total_troco)
            Venda.objects.filter(id=self.id).update(troco=total_troco)

# Somando do total de desconto da venda, por cada item e da promoção
        total_des=desconto_por_venda + desconto_por_item + total_promocao
        self.total_desconto = total_des
        Venda.objects.filter(id=self.id).update(total_desconto = total_des)

# valor da cedula
        valor_recebido = float(self.valor_recebido)
        if valor_recebido > 0 :
            cedula = float(self.valor_recebido)- total_troco
            self.valor_cedula = cedula
            Venda.objects.filter(id=self.id).update(valor_cedula = cedula)



class ItemDoPedido(models.Model):
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade_de_itens = models.DecimalField(max_digits=9, decimal_places=2, blank=True,default=1)
    desconto = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True,default=0)
    user = models.CharField(max_length=100, blank=True, null=True)
    usuarios = models.ForeignKey(Usuarios, null=True, on_delete=models.CASCADE)
   
    def __str__(self):
        return str(self.venda.id) + ' - ' + str(self.produto.nome) + ' - ' + str(self.desconto) + ' - ' + str(self.quantidade_de_itens)  + ' - ' + str(self.produto.valor_venal)

@receiver(post_save, sender=ItemDoPedido)
def update_total_saida(sender, instance, **kwargs):
    instance.produto.atualizar_estoque()

@receiver(post_save, sender=ItemDoPedido)
def update_vendas_total(sender, instance, **kwargs):
    instance.venda.calcular_total()

@receiver(post_save, sender=Venda)
def update_vendas_total2(sender, instance, **kwargs):
    instance.calcular_total()

@receiver(post_save, sender=Depositar_sacar)
def update_vendas_caixa(sender, instance, **kwargs):
    instance.caixa.caixa()
