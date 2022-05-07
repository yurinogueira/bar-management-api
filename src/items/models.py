from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from companies.models import Company
from core.behaviors import Orderable


class Item(models.Model):
    name = models.CharField("Nome", max_length=128)
    description = models.TextField("Descrição")
    attachments = GenericRelation("core.Attachment")

    class Meta:
        ordering = ("name",)
        verbose_name = "Item"
        verbose_name_plural = "Itens"

    def __str__(self) -> str:
        return self.name


class Stock(Orderable):
    item = models.ForeignKey(Item, on_delete=models.RESTRICT)
    price = models.DecimalField("Preço", max_digits=16, decimal_places=2)
    quantity = models.IntegerField("Quantidade no Estoque", default=0)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    class Meta:
        ordering = ("position",)
        verbose_name = "Estoque"
        verbose_name_plural = "Estoques"

    def __str__(self) -> str:
        return "%s - %d" % (self.item.name, self.quantity)
