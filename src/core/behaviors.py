from django.db import models
from django.utils import timezone


class Timestampable(models.Model):
    """Tracking the time of changes in an instance"""

    created_at = models.DateTimeField("Criado em", editable=False)
    updated_at = models.DateTimeField("Última atualização em", editable=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        now = timezone.localtime()

        self.created_at = self.created_at if self.created_at else now
        self.updated_at = now

        return super(Timestampable, self).save(*args, **kwargs)


class Orderable(models.Model):
    """Enable a field to be used on sort"""

    position = models.PositiveSmallIntegerField("Posição", default=0)

    class Meta:
        abstract = True
