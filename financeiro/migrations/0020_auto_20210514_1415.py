# Generated by Django 3.1.7 on 2021-05-14 14:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pessoa', '0008_auto_20210514_1345'),
        ('financeiro', '0019_auto_20210514_1036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contas',
            name='cliente',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pessoa.clientes'),
        ),
    ]
