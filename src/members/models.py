from django.db import models

from companies.models import Company
from core.behaviors import Timestampable
from members.choices import FUNCTIONS


class Member(Timestampable):
    name = models.CharField("Nome", max_length=128)
    function = models.CharField("Função", choices=FUNCTIONS, max_length=32)
    companies = models.ManyToManyField(Company)

    class Meta:
        ordering = ("-id",)
        verbose_name = "Membro"
        verbose_name_plural = "Membros"

    def __str__(self) -> str:
        return str(self.name)
