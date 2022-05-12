# Generated by Django 3.1.7 on 2021-07-20 14:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Plano',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=30)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Usuarios',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cpf_cnpj', models.CharField(max_length=30)),
                ('usuario_cliente', models.CharField(max_length=100)),
                ('razao_social', models.CharField(blank=True, max_length=30, verbose_name='Razão Social')),
                ('inscricoo_istadual', models.CharField(blank=True, max_length=30, verbose_name='Inscrição estadual')),
                ('inscricao_municipal', models.CharField(blank=True, max_length=30, verbose_name='Inscrição municipal')),
                ('nascionalidade', models.CharField(blank=True, max_length=50)),
                ('cep', models.CharField(blank=True, max_length=12)),
                ('rua', models.CharField(blank=True, max_length=50)),
                ('quadra', models.CharField(blank=True, max_length=10)),
                ('numero', models.CharField(blank=True, max_length=10, verbose_name='Número')),
                ('setor', models.CharField(blank=True, max_length=50)),
                ('estado', models.CharField(blank=True, max_length=10)),
                ('cidade', models.CharField(blank=True, max_length=10)),
                ('pais', models.CharField(blank=True, max_length=10, verbose_name='País')),
                ('complemento', models.CharField(blank=True, max_length=50)),
                ('Celular', models.CharField(blank=True, max_length=20)),
                ('DDD', models.CharField(blank=True, max_length=8)),
                ('Telefone', models.CharField(blank=True, max_length=25)),
                ('email', models.CharField(blank=True, max_length=50)),
                ('nome_fantazia', models.CharField(blank=True, max_length=50)),
                ('data_de_criacao', models.DateField(blank=True, max_length=30, null=True, verbose_name='Data de criação')),
                ('data_hora', models.DateTimeField(default=django.utils.timezone.now)),
                ('plano', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='usuarios.plano')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
