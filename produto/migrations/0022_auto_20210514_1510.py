# Generated by Django 3.1.7 on 2021-05-14 15:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pessoa', '0015_remove_clientes_sexo'),
        ('produto', '0021_auto_20210514_1415'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entradamercadoria',
            name='fornecedor',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='pessoa.fornecedor'),
        ),
    ]
