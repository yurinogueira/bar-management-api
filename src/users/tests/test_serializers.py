from django.conf import settings

import jwt
import pytest
from rest_framework import serializers

from users.serializers import ResetPasswordSerializer


@pytest.mark.django_db
class TestResetPasswordSerializer:
    def test_valid_token(self, api_client, user):
        """Ensure that when a valid token is used, instance is retrieved"""
        secret = settings.SECRET_KEY
        algorithm = settings.SIMPLE_JWT["ALGORITHM"]
        data = {"email": user.email}
        token = jwt.encode(data, secret, algorithm=algorithm)

        serializer_data = {"token": token, "password": "aSecreteWord"}
        serializer = ResetPasswordSerializer(data=serializer_data)
        serializer.is_valid(raise_exception=False)

        assert serializer.instance == user

    def test_with_invalid_user(self, api_client, user):
        """
        Ensure that when an invalid user is used, instance isn't retrieved
        """
        secret = settings.SECRET_KEY
        algorithm = settings.SIMPLE_JWT["ALGORITHM"]
        data = {"email": "email-fake@fake.com"}
        token = jwt.encode(data, secret, algorithm=algorithm)

        serializer_data = {"token": token, "password": "aSecreteWord"}
        serializer = ResetPasswordSerializer(data=serializer_data)
        serializer.is_valid(raise_exception=False)

        assert not serializer.instance

    def test_without_parameters(self, api_client):
        """Ensure that when nothing is used, nothing is retrieved"""
        serializer_data = {}
        serializer = ResetPasswordSerializer(data=serializer_data)
        serializer.is_valid(raise_exception=False)

        assert not serializer.instance

    def test_without_parameters_with_raise_exception(self, api_client):
        """Ensure that when nothing is used, error is raised!!!"""
        serializer_data = {}
        serializer = ResetPasswordSerializer(data=serializer_data)

        with pytest.raises(serializers.ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_with_invalid_user_with_raise_exception(self, api_client):
        """
        Ensure that when an invalid user is used, error is raised!!!
        """
        secret = settings.SECRET_KEY
        algorithm = settings.SIMPLE_JWT["ALGORITHM"]
        data = {"email": "fake-email@fake.com"}
        token = jwt.encode(data, secret, algorithm=algorithm)

        serializer_data = {"token": token, "password": "aSecreteWord"}
        serializer = ResetPasswordSerializer(data=serializer_data)

        with pytest.raises(serializers.ValidationError):
            serializer.is_valid(raise_exception=True)
