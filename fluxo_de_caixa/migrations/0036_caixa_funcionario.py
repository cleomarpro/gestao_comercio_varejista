# Generated by Django 3.1.7 on 2021-07-01 15:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pessoa', '0037_auto_20210630_2129'),
        ('fluxo_de_caixa', '0035_auto_20210628_1313'),
    ]

    operations = [
        migrations.AddField(
            model_name='caixa',
            name='funcionario',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='pessoa.funcionario'),
        ),
    ]
