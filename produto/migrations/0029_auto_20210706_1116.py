# Generated by Django 3.1.7 on 2021-07-06 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0028_auto_20210701_0821'),
    ]

    operations = [
        migrations.AddField(
            model_name='produto',
            name='codigo',
            field=models.CharField(default=1, max_length=13, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='produto',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
