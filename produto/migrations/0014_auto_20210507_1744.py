# Generated by Django 3.1.7 on 2021-05-07 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0013_auto_20210507_1744'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='data_inicio',
            field=models.DateField(blank=True, max_length=30, null=True),
        ),
    ]
