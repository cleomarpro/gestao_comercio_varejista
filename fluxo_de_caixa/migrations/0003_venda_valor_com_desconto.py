# Generated by Django 3.1.7 on 2021-09-27 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fluxo_de_caixa', '0002_auto_20210811_1212'),
    ]

    operations = [
        migrations.AddField(
            model_name='venda',
            name='valor_com_desconto',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=9, null=True),
        ),
    ]
