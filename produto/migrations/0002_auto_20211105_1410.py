# Generated by Django 3.1.7 on 2021-11-05 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoria',
            name='user',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='entradamercadoria',
            name='user',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='produto',
            name='user',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='promocao',
            name='user',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
