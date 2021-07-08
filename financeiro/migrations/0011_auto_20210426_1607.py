# Generated by Django 3.1.7 on 2021-04-26 19:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0010_contas_data_de_vencimento'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contas',
            name='arquivo',
        ),
        migrations.RemoveField(
            model_name='contas',
            name='data_de_vencimento',
        ),
        migrations.RemoveField(
            model_name='contas',
            name='parcelas',
        ),
        migrations.RemoveField(
            model_name='contas',
            name='parcelas_pagas',
        ),
        migrations.RemoveField(
            model_name='contas',
            name='parcelas_pago',
        ),
        migrations.RemoveField(
            model_name='contas',
            name='parcelas_restantes',
        ),
        migrations.RemoveField(
            model_name='contas',
            name='pessoa',
        ),
        migrations.RemoveField(
            model_name='contas',
            name='saldo_devedor',
        ),
        migrations.RemoveField(
            model_name='contas',
            name='tipo_de_conta',
        ),
        migrations.RemoveField(
            model_name='contas',
            name='valor',
        ),
        migrations.RemoveField(
            model_name='contas',
            name='valor_parcela',
        ),
        migrations.RemoveField(
            model_name='contas',
            name='venda',
        ),
    ]
