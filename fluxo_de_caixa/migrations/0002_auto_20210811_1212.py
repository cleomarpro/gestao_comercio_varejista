# Generated by Django 3.1.7 on 2021-08-11 12:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fluxo_de_caixa', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tipo_de_pagamento',
            name='user',
        ),
        migrations.RemoveField(
            model_name='tipo_de_pagamento',
            name='usuarios',
        ),
    ]