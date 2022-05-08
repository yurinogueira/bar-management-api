# coding: utf-8

"""Recipes to Members"""

from faker import Faker
from model_bakery.recipe import Recipe, foreign_key

from members.choices import SELLER
from members.models import Member

FAKE = Faker("pt_BR")


member = Recipe(
    Member,
    user=foreign_key("users.tests.user"),
    name=FAKE.name,
    function=SELLER,
)
