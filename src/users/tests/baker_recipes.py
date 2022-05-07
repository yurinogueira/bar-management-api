# coding: utf-8

"""Recipes to Users"""

from faker import Faker
from model_bakery.recipe import Recipe

from users.models import User

FAKE = Faker("pt_BR")


user = Recipe(
    User,
    username=FAKE.user_name,
    email=FAKE.email,
)
