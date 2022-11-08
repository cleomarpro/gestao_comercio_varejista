# DA CONTINUIDADE A UM PROJETO QUE ESTAVA EM REPOSITÓRIO DO GIT



1. crie uma pasta com o nome do projeto
2. Linux:  python3 -m  venv  nome da venv.   Windous: python -m venv myvenv (criar virtula enve na mesma pasta do projeto)
3. Linux: source NomeDaVenv/bin/activate.
    bash no windows: source NomeDaVenv/Scripts/activate,
    Windows: NomeDaVenv\Scripts\activate (ativar a venv)
4. git init (Crie um repositório git)
5. git config --global user.name "usuário" (criando usuário do git, utilizando o mesmo do github)
6. git config --global user.email "email" (E-mail do github)
7. git config --global user.name (visualizar usuário utilizado)
8. git config --global user.email(visualizar email utilizado)
9. git clone  https://github.com/cleomarpro/gestao_varejo.git (clonando o projeto na maquina local)
10. criar o arquivo .env e colocar essa chave SECRET_KEY= HgHjUyGbFbgHJmJjHmGf (arquivo para guardadr chaves)
11. pip install -r requirements.txt (comando para instalar os  requirements.txt)
10. python manage.py migrate (fazer as migrações)
11.  python manage.py createsuperuser (criar o super usuário)
12. python manage.py runserver (iniciar o servidor)

# INICIAR UM PROJETO DO ZERO

1. Criar uma pasta para o projeto
#2. Linux:  python3 -m  venv  nome da venv ou virtualenv venvGestao,  Windous: python -m venv myvenv (criar virtula enve na mesma pasta do projeto)
3. Linux=  source nome da venv/bin/activate. Windows: nome da venv\Sicrpts\activate (ativar a venv)

#3. Linux: source NomeDaVenv/bin/activate.
    bash no windows: source NomeDaVenv/Scripts/activate,
    Windows: NomeDaVenv\Scripts\activate (ativar a venv)
4. pip install django (instalação do django)
5. pip Install python3.8    ( instalar a versão mais recente do python, Obs: isso se necessário mudar a versão)
6. django-admin nome do projeto (Criar uma projeto)
7. python manage.py migrate (fazer migração)
8. python manage.py createsuperuser (criar super usuario)
9. python manage.py startapp nome da app (criar uma app)
10. python manage.py runserver (iniciar o servidor)
11 deactivate (desligar o servidor)
12 pip freeze (Visualizar os requirements.txt)
23 pip freeze > requirements.txt (Criar a pastas e os requirements.txt)

# CONFIGURAT SSH DO GIT HUB

1. Criar chave (ssh-keygen -f ~/.ssh/nome_da_chave)
2. local do arquivo chave (cd ~/.ssh/)
3. abrir o arquivo e copiar a achave (cat id_ed25519.pub)
4. acessar o gitHub, pefil > setting > chave SSH e GPG > nova chave SSH > cole a chave > em titulo, de um nome para sua chave > clique em Add SSH key
5. adicione seu repositório git (git remote add origin endereço ssh) o endereço ssh esta em, acessa o gitHub > clique no seu projeto > code > ssh e copia o endereço

# Resolvendo problemas com PIP´

1. Voltar a versção original do pip (python -m ensurepip)
2. Atualizar o pip ( python -m pip install --upgrade pip )
<<<<<<< HEAD

=======
>>>>>>> 1e52283e84f8b73e03b941dca93d72bd8ddb4969
# COMANDOS MAIS UTILIZADOS

1. python manage.py makemigrations ( prepara os dados para a migração )
2. python manage.py migrate ( migrar os dados)
3. python manage.py runserver (iniciar o servidor)
3. deactivate (desligar o servidor)
4. python manage.py createsuperuser (criar super usuario)
5. python manage.py startapp nome da app (criar uma app)
6. Linux: source NomeDaVenv/bin/activate
    Bash no windows: source NomeDaVenv/Scripts/activate,
    Windows: NomeDaVenv\Scripts\activate (ativar a venv)
7. sudo chmod -R 777 nomeDaPasta (da permissão total a determinada pasta)
8. sudo vim diretórioDoArquivo (editar arquivo no ubunto CMD)
9. 

# CONSULTAS NA ORM DO DJANGO


# Resovendo problemas comums

1. mudando um arquivo ou pasta de propietário ( chown -Rv NomeDoPropietário venvGestao )

#MANUAL GIT

-criar repositório (git init)
-Verivicar se tem algo para commitar(git status)
-preparar todos os arquivo para o commit (git add .)
-preparar um unico arquivo para o commit (git add nomeDoArquiv)
-enviar o arquivo para o repositório(git commit -m "comentáro")
-muda o repositório ou melhor "branch" (git branch -M "nome")
-criando uma nova branch "ou melhor, repositório" (git checkout -b "nomeDaNovaBranch")
-muda de branch ou repositório(git checkout 'nomeDaNovaBranch')
- juntar as branch ((git merge "nomeDaNovaBranch") em seguida (git push origin "nomeDaNovaBranch"))
-voltar voltar au estado do commit anterior incluindo as alteraçoes (git reset --hard HEAD~1)
-voltar ao estado do mommite anterrior sem alterar os arquivos modificado(git reset HEAD~1)
-tirar o arquivo adicionado a fila para o commite(git reset nomeDoArquiv)
-checar o ultimo commite, acada execução desse comado muda para o commita mais antigo (git checkout HEAD~1)
- voltar a veção anterior do arquivo (git checkout -- nomeDoArquiv)
-excluir arquivo do repositório, é nessário commitar depos da remoção (git rm caminho/arquivo_a_ser_ignorado.txt)
- incluir arquivo no gitignore apos ter comitado 
    (1: é necessário excluir o arquivo do repositório, 2:listar o arquivo no gitignore, 3:commitar novalmente)

# COMANDOS DO apache2

- /var/log/apache2$ (DIRETÓRIO DO APACHE2)

- sudo service apache2 restart (inicializar o servidor apache)
- sudo service apache2 start (parar o servidor)
sudo service apache2 status (mostrar o estado do servidor)
sudo service apache2 reload (reiniciar o servido aplicando mudanças de configuração)
- cd /var/log/apache2 nano access.log (virificar os loges do servidor)
- cd /var/log/apache2 less error.log (verificar os erros do servidor)
2 tall access.log (mostrar as ultimas linhas do arquivo de log)- cd /var/log/apache

# comandos ubunto(linux)

- sudo chmod -R 777 nomeDaPasta (da permissão total a determinada pasta)
- sudo vim diretórioDoArquivo (editar arquivo no ubunto CMD)
- mkdir nomeDaPasta (criar pasta)


# DADOS NECESSÁRIO PARA INICIAR O SISTEMA

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

Plano.objects.create(nome='Sem plano', id='1') 

Sexo.objects.create(id= '1', nome='Não espesificado') 

Sexo.objects.create(id= '2', nome='Masculino')        

Sexo.objects.create(id= '3', nome='Feminino')

Tipo_de_conta.objects.create(nome='conta a pagar', id= 2)   
Tipo_de_conta.objects.create(nome='conta a receber', id= 1)   

Promocao.objects.create(descricao='Sem promoção', id=1)
Categoria.objects.create(nome='Sem categoria', id=1)
