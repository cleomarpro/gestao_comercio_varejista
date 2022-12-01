from produto.models import Produto
from usuarios.models import Usuarios, Plano
'''
def perm_aut(funcao):
    def wrapper(request, *arg, **kwargs):
        owner = 1
        user =1
        admin =2
        cli_admin = 2
        arg2 = list(arg)
        if owner == user and admin == cli_admin:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        else:
            return render(request,'home.html')
        funcao()
    return wrapper
'''

def perm_aut():
    plano = Usuarios.objects.get(plano_id=1)
    if plano:
        return True

print(perm_aut())
  