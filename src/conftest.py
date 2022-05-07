from model_bakery import baker
import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.fixture
def user():
    return baker.make_recipe("users.tests.user")


@pytest.fixture
def member(user):
    return baker.make_recipe("members.tests.member", user=user)


@pytest.fixture
def token(member):
    refresh = RefreshToken.for_user(member.user)

    return {"refresh": str(refresh), "access": str(refresh.access_token)}


@pytest.fixture
def api_client(token):
    access = token.get("access")
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

    return client
