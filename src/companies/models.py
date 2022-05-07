from django.db import models

from localflavor.br import models as flavor_models

from core.behaviors import Timestampable


class Company(Timestampable):
    name = models.CharField("Nome", max_length=128)
    cnpj = flavor_models.BRCNPJField("CNPJ")

    class Meta:
        ordering = ("-id",)
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"

    def __str__(self) -> str:
        return str(self.name)
