# Generated by Django 3.1.7 on 2021-07-09 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0031_auto_20210707_0810'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entradamercadoria',
            name='validade_produto',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='promocao',
            name='data_inicio',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='promocao',
            name='data_termino',
            field=models.DateField(blank=True, null=True),
        ),
    ]