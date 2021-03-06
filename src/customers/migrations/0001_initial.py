# Generated by Django 3.2.13 on 2022-05-09 00:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(editable=False, verbose_name='Criado em')),
                ('updated_at', models.DateTimeField(editable=False, verbose_name='Última atualização em')),
                ('name', models.CharField(max_length=128, verbose_name='Nome')),
                ('home_credit', models.DecimalField(decimal_places=2, default=0, max_digits=16, verbose_name='Crédito na Casa')),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes',
                'ordering': ('name',),
            },
        ),
    ]
