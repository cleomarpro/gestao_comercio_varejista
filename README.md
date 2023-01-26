 DESCRIÇÃO
 
 Sistema para gestão, com foco em empresas varejistas,
Funcionalidades: Frente de caixa, caixa, controle de funcionários, conta a pagar,controle de estoque, controle de gastos e rlatório mensal anual e por produtos.

INSTRUÇÕES 
1- Baixar o repositório do GitHaub (git remote add origin URLdeOrigem)
2 - Fazer um PULL (git pull origin teste)
3 - criar uma virtualvenv (Linux:  python3 -m  venv  nome da venv.   Windous: python -m venv myvenv (criar virtula enve na mesma pasta do projeto)

4 - ativar a virtualenv (Linux: source NomeDaVenv/bin/activate.)
5- atualizar o pip (python -m pip install --upgrade pip)
6- Instalar os requirements.txt(pip install -r requirements.txt)
7- Fazer as migraçoes {python manage.py migrate}
8- Criar um super admin(python manage.py createsuperuser)

9-Dados necessários para iniciar o sistema

9.1 - Criar um grupos de permissão(python manage.py runserver --> http://127.0.0.1:8000/admin -- > faça logim e em grupos você cria os seguintes grupos ("Administrador", "Caixa","Vendedor", "Gerente", "Vendedor e Caixa", "Estoquista", Observe, sem esses grupos os novus usuários não consegue acessar o sistema))

9.2 - Execute o comando (python manage.py shell)
e depois copia os codigo abaixo e cole no terminar para criar os dados necessário para o sistem funcionar

from usuarios.models import*
from pessoa.models import*
from fluxo_de_caixa.models import*
from financeiro.models import*
from produto.models import*

Tipo_de_pagamento.objects.create(nome='Cédula', id='1')

Tipo_de_pagamento.objects.create(nome='Crédito', id='2')

Tipo_de_pagamento.objects.create(nome='Débito', id='3')

Tipo_de_pagamento.objects.create(nome='Cédula e Débito', id='4')

Tipo_de_pagamento.objects.create(nome='Cédula e Crédito', id='5')

Tipo_de_pagamento.objects.create(nome='Crédito e Débito', id='6')

Sexo.objects.create(id= '1', nome='Não espesificado')

Sexo.objects.create(id= '2', nome='Masculino')

Sexo.objects.create(id= '3', nome='Feminino')

Tipo_de_conta.objects.create(nome='conta a pagar', id='2')

Tipo_de_conta.objects.create(nome='conta a receber', id='1')

Promocao.objects.create(descricao='Sem promoção', id='1')

Categoria.objects.create(nome='Sem categoria', id='1')

Plano.objects.create(nome = 'Sem plano', id ='1')