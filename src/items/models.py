from decimal import Decimal

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone

from core.behaviors import Orderable, Timestampable
from customers.models import Customer


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

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        ordering = ("position",)
        verbose_name = "Estoque"
        verbose_name_plural = "Estoques"

    def __str__(self) -> str:
        return "%s - %d" % (self.item.name, self.quantity)


class Sell(Timestampable):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date = models.DateTimeField("Hora da Venda", default=timezone.localtime)
    is_paid = models.BooleanField("Venda Paga", default=True)
    discount = models.DecimalField(
        "Desconto",
        max_digits=16,
        decimal_places=2,
        default=0,
    )
    amount_paid = models.DecimalField(
        "Valor Pago",
        max_digits=16,
        decimal_places=2,
        default=0,
    )

    stocks = GenericRelation("items.Stock")

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Venda"
        verbose_name_plural = "Vendas"

    @property
    def total_price(self) -> Decimal:
        try:
            stocks = self.prefetched_stocks
        except AttributeError:
            stocks = self.stocks

        # Sum stocks cost and apply the discount
        stocks_price = sum((stock.price * stock.price) for stock in stocks)
        discount_value = stocks_price * (self.discount / 100)
        return stocks_price - discount_value

    def __str__(self) -> str:
        return "%s - %s" % (self.total_price, self.date.isoformat())
