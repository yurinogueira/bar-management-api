from unittest import mock

import jwt
import pytest
from django.conf import settings
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestResetPasswordViewSet:
    @pytest.fixture
    def payload(self, user):
        secret = settings.SECRET_KEY
        algorithm = settings.SIMPLE_JWT["ALGORITHM"]
        data = {"email": user.email}
        token = jwt.encode(data, secret, algorithm=algorithm)

        return {"token": token, "password": "aSecreteWord"}

    @pytest.fixture
    def m_serializer(self, user, payload):
        with mock.patch("users.serializers.ResetPasswordSerializer") as mocked:
            mocked.is_valid.return_value = True
            mocked.data.return_value = payload
            mocked.instance.return_value = user
            yield mocked

    def test_post(self, m_serializer, payload, api_client, user):
        url = reverse("users:reset-password")
        response = api_client.post(url, payload)

        assert response.status_code == status.HTTP_200_OK
