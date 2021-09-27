# Generated by Django 3.1.7 on 2021-09-27 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fluxo_de_caixa', '0003_venda_valor_com_desconto'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='venda',
            name='nota_fiscal_impressa',
        ),
        migrations.AddField(
            model_name='venda',
            name='nfe_emitida',
            field=models.BooleanField(default=False),
        ),
    ]
