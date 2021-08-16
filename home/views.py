from django.shortcuts import render
#from django.conf import settings
#from django.shortcuts import redirect #, render
from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib.auth.models import User
from usuarios.models import Usuarios, Plano

def home(request):
    return render(request,'home.html')
@login_required()
def TelaInicial(request):
    return render(request,'tela_inicial.html')

class Usuario(View):
    def get(self, request):
        user_logado = request.user # Obitendo o usuário logado
        user_logado = user_logado.id # obitendo o ID do usuário logado
        if Usuarios.objects.filter(user_id = user_logado):
            usuario = Usuarios.objects.get(user_id = user_logado)
            return render(request,'usuario.html', {'usuario': usuario})
        else:
            return render(request,'funcionario.html')
