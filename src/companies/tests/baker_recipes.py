# coding: utf-8

"""Recipes to Companies"""

from faker import Faker
from model_bakery.recipe import Recipe

from companies.models import Company

FAKE = Faker("pt_BR")


company = Recipe(
    Company,
    name=FAKE.bs,
    cnpj=FAKE.cnpj,
)
