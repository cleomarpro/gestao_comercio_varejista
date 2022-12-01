from django import forms
from .models import  Produto, fornecedor
from django.forms import ModelForm

class ProdutoForm(ModelForm):
    class Meta:
        model = Produto
        fields = '__all__'

class entrada_de_MercadoriaForm(forms.Form):
    produto_id = forms.ModelMultipleChoiceField(queryset = Produto.objects.all().order_by("nome"))
    Fornecedor_id = forms.ModelMultipleChoiceField(queryset = fornecedor.objects.all().order_by("nome"))
    quantidade = forms.CharField(label='Categoria', max_length=100)
    #ggg = forms.CharField(label='Categoria', max_length=100)
    #comment = forms.CharField(widget=forms.TextInput(attrs={'size': '40'}))