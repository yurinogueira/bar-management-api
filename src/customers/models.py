from django.db import models

from core.behaviors import Timestampable


class Customer(Timestampable):
    name = models.CharField("Nome", max_length=128)
    home_credit = models.DecimalField(
        "Crédito na Casa",
        max_digits=16,
        decimal_places=2,
        default=0,
    )

    class Meta:
        ordering = ("name",)
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def __str__(self) -> str:
        return str(self.name)
