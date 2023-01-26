from django import forms
from .models import  Produto
from .models import ItemDoPedido

#from django.core.exceptions import ValidationError
#from django.forms import Select #CheckboxInput, ModelChoiceField, Select, ModelMultipleChoiceField, SelectMultiple
#from django.utils.translation import ugettext_lazy as _
class ItemPedidoValidacaoForm(forms.Form):
    produto_id = forms.CharField(label='Código', max_length=100)

def produtoID(valor, request):
    produto= ItemDoPedido.objects.filter(produto_id=request.POST['produto_id']) or 0
    if produto == 0:
        raise forms.ValidationError('Produto não cadastrado')

class ItemPedidoForm(forms.Form):
    produto_id = forms.CharField( validators=[produtoID, ])
    #produto_id = forms.CharField(label='Código', max_length=100)
    #busca= forms.CharField(label='Buscar produtos', max_length=100)
    #produto_id = forms.ModelMultipleChoiceField(queryset=Produto.objects.all().order_by("nome"))

    def clean_produto_id(self):
        produto = self.cleaned_data['produto_id']
        valor = Produto.objects.filter(id=produto)
        if "produto_id" not in valor:
            raise forms.ValidationError('Produto não cadastrado')
        return produto

#https://books.google.com.br/books?id=ma3_DwAAQBAJ&pg=PT439&lpg=PT439&dq=MultipleChoiceField+django+busca&source=bl&ots=Wfgox97M8B&sig=ACfU3U0GpXXmG1yV6hO6V_B0W0kfho4WdA&hl=pt-BR&sa=X&ved=2ahUKEwji59WCm4zvAhX9G7kGHd9sCVcQ6AEwEXoECBgQAw#v=onepage&q=MultipleChoiceField%20django%20busca&f=false
#https://pythonacademy.com.br/blog/desenvolva-aplicativos-para-android-ios-com-python-e-kivy
#https://data-flair.training/blogs/django-forms-handling-and-validation/
#https://django.readthedocs.io/en/stable/topics/forms/modelforms.html
#https://django.readthedocs.io/en/stable/ref/models/instances.html#validating-objects