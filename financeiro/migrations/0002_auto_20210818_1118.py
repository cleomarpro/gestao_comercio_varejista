# Generated by Django 3.1.7 on 2021-08-18 11:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tipo_de_conta',
            name='user',
        ),
        migrations.RemoveField(
            model_name='tipo_de_conta',
            name='usuarios',
        ),
    ]
