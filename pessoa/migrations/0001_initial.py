# Generated by Django 3.1.7 on 2021-03-20 13:08

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='cidade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(blank=True, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Contato',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Celular', models.CharField(blank=True, max_length=20)),
                ('Telefone', models.CharField(blank=True, max_length=25)),
                ('email', models.CharField(blank=True, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Departamento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(blank=True, max_length=50)),
                ('data_hora', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Endereco',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(blank=True, max_length=50)),
                ('nascionalidade', models.CharField(blank=True, max_length=50)),
                ('rua', models.CharField(blank=True, max_length=50)),
                ('quadra', models.CharField(blank=True, max_length=10)),
                ('numero', models.CharField(blank=True, max_length=10)),
                ('setor', models.CharField(blank=True, max_length=50)),
                ('cidade', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='pessoa.cidade')),
            ],
        ),
        migrations.CreateModel(
            name='Estado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(blank=True, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Pais',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(blank=True, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Parentesco',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(blank=True, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Pessoa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contato', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='pessoa.contato')),
                ('endereco', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='pessoa.endereco')),
            ],
        ),
        migrations.CreateModel(
            name='Sexo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(blank=True, max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='cliente',
            fields=[
                ('pessoa_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='pessoa.pessoa')),
                ('nome', models.CharField(blank=True, max_length=50)),
                ('segundo_nome', models.CharField(blank=True, max_length=50)),
                ('cpf', models.CharField(blank=True, max_length=11)),
                ('data_de_nascimento', models.CharField(blank=True, max_length=11)),
            ],
            bases=('pessoa.pessoa',),
        ),
        migrations.CreateModel(
            name='fornecedor',
            fields=[
                ('pessoa_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='pessoa.pessoa')),
                ('nome', models.CharField(blank=True, max_length=50)),
                ('cnpj', models.CharField(blank=True, max_length=20)),
                ('data_de_criacao', models.CharField(blank=True, max_length=11)),
            ],
            bases=('pessoa.pessoa',),
        ),
        migrations.AddField(
            model_name='pessoa',
            name='sexo',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='pessoa.sexo'),
        ),
        migrations.AddField(
            model_name='endereco',
            name='estado',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='pessoa.estado'),
        ),
        migrations.AddField(
            model_name='endereco',
            name='pais',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='pessoa.pais'),
        ),
        migrations.CreateModel(
            name='Funcionario',
            fields=[
                ('pessoa_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='pessoa.pessoa')),
                ('nome', models.CharField(blank=True, max_length=50)),
                ('segundo_nome', models.CharField(blank=True, max_length=50)),
                ('cpf', models.CharField(blank=True, max_length=11)),
                ('data_de_nascimento', models.CharField(blank=True, max_length=11)),
                ('departamento', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='pessoa.departamento')),
                ('parentesco', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='pessoa.parentesco')),
            ],
            bases=('pessoa.pessoa',),
        ),
    ]
