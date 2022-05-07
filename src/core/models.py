import uuid

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.files.storage import get_storage_class
from django.db import models

from core.behaviors import Orderable, Timestampable
from core.choices import FILE, FILE_TYPES


def set_directory_path(instance, filename):
    app = instance.content_type.app_label
    model = instance.content_type.model
    owner = instance.content_object.id

    return "attachments/{0}/{1}/{2}/{3}".format(app, model, owner, filename)


class Attachment(Timestampable, Orderable):
    uuid = models.UUIDField(
        "Identificador",
        default=uuid.uuid4,
        editable=False,
        unique=True,
        db_index=True,
    )
    name = models.CharField("Nome", max_length=255)
    file = models.FileField(
        "Anexo",
        upload_to=set_directory_path,
        storage=get_storage_class(),
    )
    type = models.CharField(
        "Tipo de Arquivo",
        max_length=25,
        choices=FILE_TYPES,
        default=FILE,
    )

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Anexo"
        verbose_name_plural = "Anexos"
        ordering = (
            "position",
            "-created_at",
        )
