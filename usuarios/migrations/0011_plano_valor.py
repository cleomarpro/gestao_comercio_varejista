# Generated by Django 3.1.7 on 2023-01-22 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0010_auto_20230122_0818'),
    ]

    operations = [
        migrations.AddField(
            model_name='plano',
            name='valor',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=9),
        ),
    ]
