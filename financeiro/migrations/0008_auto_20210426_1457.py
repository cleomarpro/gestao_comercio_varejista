# Generated by Django 3.1.7 on 2021-04-26 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0007_auto_20210426_1455'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contas',
            name='parcelas',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=9),
        ),
        migrations.AlterField(
            model_name='contas',
            name='parcelas_restantes',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=9),
        ),
    ]
