# Generated by Django 3.1.7 on 2021-03-30 01:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fluxo_de_caixa', '0008_venda_finalizada'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='venda',
            name='nota_fiscal_emitida',
        ),
        migrations.RemoveField(
            model_name='venda',
            name='pago',
        ),
        migrations.AddField(
            model_name='venda',
            name='nota_fiscal_impressa',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
