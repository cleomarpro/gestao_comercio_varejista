# Generated by Django 3.1.7 on 2021-11-10 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0002_parcelasconta'),
    ]

    operations = [
        migrations.AddField(
            model_name='parcelasconta',
            name='Juros',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=9, null=True),
        ),
        migrations.AddField(
            model_name='parcelasconta',
            name='user',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
