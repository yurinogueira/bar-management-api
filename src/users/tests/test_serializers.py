from django.conf import settings

import jwt
from model_bakery import baker
import pytest
from rest_framework import serializers

from users.models import User
from users.serializers import ResetPasswordSerializer, UserSerializer


@pytest.mark.django_db
class TestResetPasswordSerializer:
    def test_valid_token(self, user):
        """Ensure that when a valid token is used, instance is retrieved"""
        secret = settings.SECRET_KEY
        algorithm = settings.SIMPLE_JWT["ALGORITHM"]
        data = {"email": user.email}
        token = jwt.encode(data, secret, algorithm=algorithm)

        serializer_data = {"token": token, "password": "aSecreteWord"}
        serializer = ResetPasswordSerializer(data=serializer_data)
        serializer.is_valid(raise_exception=False)

        assert serializer.instance == user

    def test_with_invalid_user(self):
        """Ensure that when an invalid user, instance isn't retrieved"""
        secret = settings.SECRET_KEY
        algorithm = settings.SIMPLE_JWT["ALGORITHM"]
        data = {"email": "email-fake@fake.com"}
        token = jwt.encode(data, secret, algorithm=algorithm)

        serializer_data = {"token": token, "password": "aSecreteWord"}
        serializer = ResetPasswordSerializer(data=serializer_data)
        serializer.is_valid(raise_exception=False)

        assert not serializer.instance

    def test_without_parameters(self):
        """Ensure that when nothing is used, nothing is retrieved"""
        serializer_data = {}
        serializer = ResetPasswordSerializer(data=serializer_data)
        serializer.is_valid(raise_exception=False)

        assert not serializer.instance

    def test_without_parameters_with_raise_exception(self):
        """Ensure that when nothing is used, error is raised!!!"""
        serializer_data = {}
        serializer = ResetPasswordSerializer(data=serializer_data)

        with pytest.raises(serializers.ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_with_invalid_user_with_raise_exception(self):
        """Ensure that when an invalid user, error is raised!!!"""
        secret = settings.SECRET_KEY
        algorithm = settings.SIMPLE_JWT["ALGORITHM"]
        data = {"email": "fake-email@fake.com"}
        token = jwt.encode(data, secret, algorithm=algorithm)

        serializer_data = {"token": token, "password": "aSecreteWord"}
        serializer = ResetPasswordSerializer(data=serializer_data)

        with pytest.raises(serializers.ValidationError):
            serializer.is_valid(raise_exception=True)


@pytest.mark.django_db
class TestUserSerializer:
    def test_retrieve_user(self, user):
        """Ensure that user data is retrieved"""
        serializer = UserSerializer(user)

        assert serializer.data["username"] == user.username

    def test_retrieve_many(self):
        """Ensure that multiple users are retrieved"""
        quantity = 3
        baker.make_recipe("users.tests.user", _quantity=quantity)
        serializer = UserSerializer(User.objects.all(), many=True)

        assert len(serializer.data) == quantity
