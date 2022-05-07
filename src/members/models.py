from django.db import models

from core.behaviors import Timestampable
from members.choices import FUNCTIONS


class Member(Timestampable):
    user = models.OneToOneField("users.User", on_delete=models.CASCADE)
    name = models.CharField("Nome", max_length=128)
    function = models.CharField("Função", choices=FUNCTIONS, max_length=32)
    companies = models.ManyToManyField("companies.Company")

    class Meta:
        ordering = ("name",)
        verbose_name = "Membro"
        verbose_name_plural = "Membros"

    def __str__(self) -> str:
        return str(self.name)
