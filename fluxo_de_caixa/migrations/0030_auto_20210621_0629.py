# Generated by Django 3.1.7 on 2021-06-21 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fluxo_de_caixa', '0029_depositar_sacar_data_hora'),
    ]

    operations = [
        migrations.AlterField(
            model_name='depositar_sacar',
            name='descricao',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Descrição'),
        ),
    ]
