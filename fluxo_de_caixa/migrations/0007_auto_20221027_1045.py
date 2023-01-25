# Generated by Django 3.1.7 on 2022-10-27 10:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pessoa', '0009_remove_pessoa_user_2'),
        ('fluxo_de_caixa', '0006_itemdopedido_estoque_fisico_atual'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='venda',
            name='descricao',
        ),
        migrations.AddField(
            model_name='venda',
            name='cliente',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='pessoa.cliente'),
        ),
    ]
