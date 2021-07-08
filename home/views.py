from django.shortcuts import render
#from django.conf import settings
#from django.shortcuts import redirect #, render
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request,'home.html')
@login_required()
def TelaInicial(request):
    return render(request,'tela_inicial.html')

@login_required()
def usuario(request):
    return render(request,'usuario.html')