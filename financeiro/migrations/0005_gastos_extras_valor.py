# Generated by Django 3.1.7 on 2021-11-11 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0004_remove_gastos_extras_valor'),
    ]

    operations = [
        migrations.AddField(
            model_name='gastos_extras',
            name='valor',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=9),
        ),
    ]