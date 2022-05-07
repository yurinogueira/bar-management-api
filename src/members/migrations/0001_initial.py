# Generated by Django 3.2.13 on 2022-05-07 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('companies', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(editable=False, verbose_name='Criado em')),
                ('updated_at', models.DateTimeField(editable=False, verbose_name='Última atualização em')),
                ('name', models.CharField(max_length=128, verbose_name='Nome')),
                ('function', models.CharField(choices=[('manager', 'Gerente'), ('seller', 'Balconista'), ('accountant', 'Contabilista')], max_length=32, verbose_name='Função')),
                ('companies', models.ManyToManyField(to='companies.Company')),
            ],
            options={
                'verbose_name': 'Membro',
                'verbose_name_plural': 'Membros',
                'ordering': ('name',),
            },
        ),
    ]
