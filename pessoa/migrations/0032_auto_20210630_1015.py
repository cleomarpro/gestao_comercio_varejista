# Generated by Django 3.1.7 on 2021-06-30 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pessoa', '0031_pessoa_usuario_cliente'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pessoa',
            name='usuario_cliente',
            field=models.CharField(max_length=100),
        ),
    ]
