from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from usuarios.models import Usuarios


class Sexo (models.Model):
    nome = models.CharField(max_length=30,  blank=True)
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    #usuarios = models.ForeignKey(Usuarios, null=True, on_delete=models.CASCADE)

    def __str__(self): # METODO CONSTRUTOR
       return str(self.nome) + ' - ' + str(self.id)


class Pessoa (models.Model):
    nascionalidade = models.CharField(max_length=50,blank=True)
    cep = models.CharField(max_length=12,blank=True)
    rua = models.CharField(max_length=50,blank=True)
    quadra = models.CharField(max_length=10,blank=True)
    numero = models.CharField(max_length=10,blank=True,verbose_name="Número")
    setor = models.CharField(max_length=50,blank=True)
    estado = models.CharField(max_length=10,blank=True)
    cidade = models.CharField(max_length=10,blank=True)
    pais = models.CharField(max_length=10,blank=True, verbose_name="País")
    complemento = models.CharField(max_length=50,blank=True)
    Celular = models.CharField(max_length=20,blank=True)
    Celular2 = models.CharField(max_length=20,blank=True)
    Telefone = models.CharField(max_length=25,blank=True)
    email = models.CharField(max_length=50,blank=True)
    usuarios = models.ForeignKey(Usuarios, null=True, on_delete=models.CASCADE)


class Departamento (models.Model):
    nome = models.CharField(max_length=50,blank=True)
    data_hora = models.DateTimeField(default=timezone.now)
    user = models.CharField(max_length=100,blank=True, null=True)
    usuarios = models.ForeignKey(Usuarios, null=True, on_delete=models.CASCADE)


    def __str__(self): # METODO CONSTRUTOR
       return self.segundo_nome

class Funcionario (Pessoa):
    nome = models.CharField(max_length=50,blank=True)
    segundo_nome = models.CharField(max_length=50,blank=True)
    cpf = models.CharField(max_length=15,blank=True)
    data_de_nascimento = models.DateField(max_length=30, null= True, blank=True)
    sexo = models.ForeignKey(Sexo, on_delete=models.CASCADE, default=1)
    departamento = models.ForeignKey
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    def __str__(self): # METODO CONSTRUTOR
       return str(self.nome)+ ' ' + str(self.cpf)

class Cliente (Pessoa):
    nome = models.CharField(max_length=50,blank=True)
    segundo_nome = models.CharField(max_length=50,blank=True)
    cpf_cnpj = models.CharField(max_length=30,blank=True)
    data_de_nascimento= models.DateField(max_length=30, null= True, blank=True)
    sexo = models.ForeignKey(Sexo, on_delete=models.CASCADE, default=1)
    user = models.CharField(max_length=100,blank=True, null=True)


    def __str__(self): # METODO CONSTRUTOR
       return  str(self.nome)+ ' - ' + str(self.cpf_cnpj)

class Fornecedor (Pessoa):
    nome_fantazia = models.CharField(max_length=50,blank=True)
    cnpj = models.CharField(max_length=20,blank=True)
    data_de_criacao = models.DateField(max_length=30, null= True, blank=True, verbose_name="Data de criação")
    user = models.CharField(max_length=100,blank=True, null=True)


    def __str__(self): # METODO CONSTRUTOR
       return str(self.nome_fantazia)+ ' - ' + str(self.cnpj)

