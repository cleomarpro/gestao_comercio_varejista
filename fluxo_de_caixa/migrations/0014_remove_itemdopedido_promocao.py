# Generated by Django 3.1.7 on 2021-04-21 19:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fluxo_de_caixa', '0013_auto_20210421_0956'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='itemdopedido',
            name='promocao',
        ),
    ]
