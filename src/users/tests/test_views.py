from unittest import mock

from django.conf import settings
from django.urls import reverse

import jwt
from model_bakery import baker
import pytest
from rest_framework import status

from users.models import User


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
        """Ensure that post router works"""
        url = reverse("users:reset-password")
        response = api_client.post(url, payload)

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestUserViewSet:
    @pytest.fixture
    def o_member(self):
        return baker.make_recipe(
            "members.tests.member",
            user=baker.make_recipe("users.tests.user"),
        )

    @pytest.fixture
    def company(self):
        return baker.make_recipe("companies.tests.company")

    def test_get(self, api_client, user):
        """Ensure that when a valid username, user is retrieved"""
        url = reverse("users:user-detail", args=[user.username])
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK

    def test_get_same_company(self, api_client, user, company, o_member):
        """Ensure that when in same company, user is retrieved"""
        company.member_set.add(user.member)
        company.member_set.add(o_member)

        url = reverse("users:user-detail", args=[o_member.user.username])
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK

    def test_get_should_raise_not_found(self, api_client, user):
        """Ensure that when an invalid username, nothing is retrieved"""
        url = reverse("users:user-detail", args=[user.email])
        response = api_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_other_should_raise_not_found(self, api_client, user):
        """Ensure that a user can't retrieve other users"""
        debug_user = baker.make_recipe("users.tests.user")
        url = reverse("users:user-detail", args=[debug_user.username])
        response = api_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_staff_get_other(self, api_client, user):
        """Ensure that a staff can retrieve other users"""
        user.is_staff = True
        user.is_superuser = True
        user.save(update_fields=["is_staff", "is_superuser"])

        debug_user = baker.make_recipe("users.tests.user")
        url = reverse("users:user-detail", args=[debug_user.username])
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK

    def test_list(self, api_client, user):
        """Ensure that user can retrieve onlyself"""
        url = reverse("users:user-list")
        response = api_client.get(url)

        assert response.data["count"] == 1
        assert response.status_code == status.HTTP_200_OK

    def test_list_same_company(self, api_client, user, company, o_member):
        """Ensure that when in same company, all users are retrieved"""
        company.member_set.add(user.member)
        company.member_set.add(o_member)

        url = reverse("users:user-list")
        response = api_client.get(url)

        assert response.data["count"] == 2
        assert response.status_code == status.HTTP_200_OK

    def test_staff_list(self, api_client, user, o_member):
        """Ensure that a staff can retrieve all users"""
        user.is_staff = True
        user.is_superuser = True
        user.save(update_fields=["is_staff", "is_superuser"])

        baker.make_recipe("users.tests.user")
        url = reverse("users:user-list")
        response = api_client.get(url)

        assert response.data["count"] == User.objects.count()
        assert response.status_code == status.HTTP_200_OK
