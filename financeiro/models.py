from django.db import models
from django.utils import timezone
#from django.db.models import Sum, F, FloatField #Max ExpressionWrapper ExpressionWrapper, #funções agrega
from django.db.models.signals import post_save
from django.dispatch import receiver
from pessoa.models import Cliente
from fluxo_de_caixa.models import Venda
from django.contrib.auth.models import User
from usuarios.models import Usuarios
from django.db.models import Sum
#import datetime
#from django.utils import timezone

class Relatorios(models.Model):
    descricao=models.CharField(max_length=100, blank=True, verbose_name="Descrição")
    def __str__(self): # METODO CONSTRUTOR
        return self.descricao

class GastosExtrasCategoria(models.Model):
    nome=models.CharField(max_length=30, blank=True, null=True, verbose_name="Nome")
    user = models.CharField(max_length=30, blank=True, null=True, verbose_name="Funcionário")
    usuarios = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    def __str__(self): # METODO CONSTRUTOR
        return self.nome

class Gastos_extras(models.Model):
    descricao=models.CharField(max_length=100, blank=True, verbose_name="Descrição")
    valor = models.DecimalField(max_digits=9, decimal_places=2, blank=False, default=0)
    data_hora = models.DateTimeField(default=timezone.now)
    gastosExtrasCategoria = models.ForeignKey(GastosExtrasCategoria, blank=True, null=True, on_delete=models.CASCADE)
    arquivo = models.FileField(default=False, blank=True)
    user = models.CharField(max_length=100,null=True, blank=True)
    usuarios = models.ForeignKey(Usuarios, on_delete=models.CASCADE)

    def __str__(self): # METODO CONSTRUTOR
        return self.descricao + ' - ' + self.valor

class Tipo_de_conta(models.Model):
    nome=models.CharField(max_length=50, blank=True)
    

    def __str__(self): # METODO CONSTRUTOR
       return self.nome

class Contas(models.Model):
    observacao = models.CharField(max_length=100, blank=True, verbose_name="Observação")
    cliente = models.ForeignKey(Cliente, null=True, blank=True, on_delete=models.CASCADE)
    venda = models.ForeignKey(Venda, null=True, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=9, decimal_places=2, blank=False, default=0)
    valor_com_juros = models.DecimalField(max_digits=9, decimal_places=2, blank=False, null=True, default=0)
    valor_parcela = models.DecimalField(max_digits=9, decimal_places=2, blank=False, default=0)
    parcelas_pagas = models.DecimalField(max_digits=9, decimal_places=0, blank=False, default=0)
    parcelas = models.DecimalField(max_digits=9, decimal_places=0, blank=False, default=0)
    saldo_devedor = models.DecimalField(max_digits=9, decimal_places=2, blank=False, default=0)
    parcelas_restantes = models.DecimalField(max_digits=9, decimal_places=0, blank=False, default=0)
    juros = models.DecimalField(max_digits=9, decimal_places=2, blank=False, null=True, default=0)
    tipo_de_conta = models.ForeignKey(Tipo_de_conta, on_delete=models.CASCADE)
    data_de_vencimento =models.DateField(default=False, blank=True)
    data_hora = models.DateTimeField(default=timezone.now)
    arquivo = models.FileField(default=False, blank=True)
    user_2 = models.CharField(max_length=100,null=True, blank=True)
    user = models.CharField(max_length=100,null=True, blank=True)
    usuarios = models.ForeignKey(Usuarios, on_delete=models.CASCADE)

    def __str__(self): # METODO CONSTRUTOR
       return str(self.cliente) + ' - ' + str(self.parcelas_restantes)+ ' - ' + str(self.valor)

    def total_contas(self):
#Calculo do valor com juros
        if float(self.juros) > 0 :
            juros= float(self.juros) / 100 #obtendo juros em porcentagem
            total_de_parcela= float(self.parcelas) 
            valor_do_debito= float(self.valor)
            total_valor_com_juros = ((1 + juros)**total_de_parcela - 1) / ((1 + juros)**total_de_parcela * juros)
            total_valor_com_juros = valor_do_debito / total_valor_com_juros * total_de_parcela
            #total_valor_com_juros = valor_do_debito * (1 + juros)**total_de_parcela # Juros composto
            # total_valor_com_juros = float(self.valor) * float(self.juros) / 100 juros simples
            # total_valor_com_juros = total_valor_com_juros + float(self.valor) # juros simples
            self.valor_com_juros = total_valor_com_juros
            Contas.objects.filter(id=self.id).update(valor_com_juros = total_valor_com_juros)

# Calculo do valor da parcela
        valor_da_parcela = float(self.valor_com_juros) / float(self.parcelas) 
        self.valor_parcela = float(valor_da_parcela)
        Contas.objects.filter(id=self.id).update(valor_parcela = valor_da_parcela)

#pagamento
        pagamento = self.pagamento_set.all().aggregate(total_parcelas = Sum('quantidade_de_parcelas'))
        totalParcelas = pagamento['total_parcelas'] or 0
        self.parcelas_pagas = totalParcelas
        Contas.objects.filter(id=self.id).update(parcelas_pagas = totalParcelas)

# Calcula das parcelas restantes
        parcelasRestantes = float(self.parcelas) - float(totalParcelas)
        self.parcelas_restantes = float(parcelasRestantes)
        Contas.objects.filter(id=self.id).update(parcelas_restantes = parcelasRestantes)

# Calculo do saldo devedor
        saldoDevedor = float(self.valor_com_juros) / float(self.parcelas) * float(self.parcelas_restantes)
        self.saldo_devedor = float(saldoDevedor)
        Contas.objects.filter(id=self.id).update(saldo_devedor = saldoDevedor)

class Pagamento(models.Model):
    observacao = models.CharField(max_length=100, blank=True, verbose_name="Observação")
    quantidade_de_parcelas = models.DecimalField(max_digits=9, decimal_places=0, blank=False, default=0)
    contas = models.ForeignKey(Contas, on_delete=models.CASCADE)
    total_pago = models.DecimalField(max_digits=9, decimal_places=0, blank=False, default=0)
    data_hora = models.DateTimeField(default=timezone.now)
    user = models.CharField(max_length=100,null=True, blank=True)
    usuarios = models.ForeignKey(Usuarios, on_delete=models.CASCADE)

# Valor pago
    def pagamento(self):
        valorPago = float(self.quantidade_de_parcelas) * float(self.contas.valor_parcela)
        self.total_pago = valorPago
        Pagamento.objects.filter(id=self.id).update(total_pago = valorPago)

    def __str__(self): # METODO CONSTRUTOR
       return str(self.quantidade_de_parcelas)  + ' - ' + str(self.contas.parcelas_restantes) + ' - ' + str(self.contas.valor_parcela)

class ParcelasConta(models.Model):
    usuarios = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    user = models.CharField(max_length=100,null=True, blank=True)
    numero_da_parcelas = models.CharField(max_length=100,null=True, blank=True)
    data_de_vencimento =models.DateField(default=False, blank=True)
    contas = models.ForeignKey(Contas, on_delete=models.CASCADE)

@receiver(post_save, sender= Contas)
def update_total_contas(sender, instance, **kwargs):
    instance.total_contas()

@receiver(post_save, sender= Pagamento)
def update_total_conta(sender, instance, **kwargs):
    instance.contas.total_contas()

@receiver(post_save, sender= Pagamento)
def update_pagamento(sender, instance, **kwargs):
    instance.pagamento()







