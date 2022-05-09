# Generated by Django 3.2.13 on 2022-05-09 00:34

import core.models
import django.core.files.storage
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(editable=False, verbose_name='Criado em')),
                ('updated_at', models.DateTimeField(editable=False, verbose_name='Última atualização em')),
                ('position', models.PositiveSmallIntegerField(default=0, verbose_name='Posição')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True, verbose_name='Identificador')),
                ('name', models.CharField(max_length=255, verbose_name='Nome')),
                ('file', models.FileField(storage=django.core.files.storage.FileSystemStorage, upload_to=core.models.set_directory_path, verbose_name='Anexo')),
                ('type', models.CharField(choices=[('video', 'Video'), ('image', 'Imagem'), ('file', 'Arquivo'), ('thumbnail', 'Miniatura')], default='file', max_length=25, verbose_name='Tipo de Arquivo')),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
            options={
                'verbose_name': 'Anexo',
                'verbose_name_plural': 'Anexos',
                'ordering': ('position', '-created_at'),
            },
        ),
    ]
