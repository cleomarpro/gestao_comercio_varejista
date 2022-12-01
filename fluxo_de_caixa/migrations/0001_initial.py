# Generated by Django 3.1.7 on 2021-07-20 14:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pessoa', '0001_initial'),
        ('usuarios', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('produto', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Caixa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_do_caixa', models.CharField(max_length=30)),
                ('valor_atualizado', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=9, null=True)),
                ('funcionario', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='pessoa.funcionario')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('usuarios', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='usuarios.usuarios')),
            ],
        ),
        migrations.CreateModel(
            name='Tipo_de_pagamento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=30)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('usuarios', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='usuarios.usuarios')),
            ],
        ),
        migrations.CreateModel(
            name='Venda',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=9, null=True)),
                ('desconto', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=9, null=True)),
                ('total_desconto', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=9, null=True)),
                ('valor_recebido', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=9, null=True)),
                ('valor_credito', models.FloatField(blank=True, default=0, null=True)),
                ('valor_cedula', models.FloatField(blank=True, default=0, null=True)),
                ('valor_debito', models.FloatField(blank=True, default=0, null=True)),
                ('troco', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=9, null=True)),
                ('descricao', models.CharField(blank=True, max_length=100)),
                ('finalizada', models.CharField(blank=True, max_length=20)),
                ('nota_fiscal_impressa', models.CharField(blank=True, max_length=20)),
                ('data_hora', models.DateTimeField(default=django.utils.timezone.now)),
                ('tipo_de_pagamento', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='fluxo_de_caixa.tipo_de_pagamento')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('usuarios', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='usuarios.usuarios')),
            ],
        ),
        migrations.CreateModel(
            name='ItemDoPedido',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade_de_itens', models.DecimalField(blank=True, decimal_places=2, default=1, max_digits=9)),
                ('desconto', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=9, null=True)),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='produto.produto')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('usuarios', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='usuarios.usuarios')),
                ('venda', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fluxo_de_caixa.venda')),
            ],
        ),
        migrations.CreateModel(
            name='Depositar_sacar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(blank=True, max_length=100, null=True, verbose_name='Descrição')),
                ('estadoDoCaixa', models.CharField(blank=True, max_length=10, null=True, verbose_name='Descrição')),
                ('depositar', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=9, null=True)),
                ('venda_realizadas', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=9, null=True)),
                ('saldo_em_caixa', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=9, null=True)),
                ('sacar', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=9, null=True)),
                ('data_hora', models.DateTimeField(default=django.utils.timezone.now)),
                ('caixa', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='fluxo_de_caixa.caixa')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('usuarios', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='usuarios.usuarios')),
            ],
        ),
    ]
