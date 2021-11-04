# Generated by Django 3.1.7 on 2021-11-03 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0006_gastos_extras_gastosextrascategoria'),
    ]

    operations = [
        migrations.AddField(
            model_name='gastosextrascategoria',
            name='user',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Funcionário'),
        ),
        migrations.AddField(
            model_name='gastosextrascategoria',
            name='usuarios',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Usuário'),
        ),
        migrations.AlterField(
            model_name='gastosextrascategoria',
            name='nome',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Nome'),
        ),
    ]
