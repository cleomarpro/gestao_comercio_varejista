# Generated by Django 3.1.7 on 2021-07-09 13:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0032_auto_20210709_1014'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='produto',
            name='inicio_da_promocao',
        ),
        migrations.RemoveField(
            model_name='produto',
            name='termino_da_promocao',
        ),
    ]
