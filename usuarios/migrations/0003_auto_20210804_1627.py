# Generated by Django 3.1.7 on 2021-08-04 16:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0002_auto_20210804_1622'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usuarios',
            old_name='inscricao_istadual',
            new_name='inscricao_estadual',
        ),
    ]
