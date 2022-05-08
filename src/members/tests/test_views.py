from django.urls import reverse

from faker import Faker
from model_bakery import baker
import pytest
from rest_framework import status

from members.choices import MANAGER
from users.models import Member

FAKE = Faker("pt_BR")


@pytest.mark.django_db
class TestMemberViewSet:
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
        """Ensure that when a valid username, member is retrieved"""
        url = reverse("members:member-detail", args=[user.username])
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK

    def test_get_same_company(self, api_client, user, company, o_member):
        """Ensure that when in same company, member is retrieved"""
        company.member_set.add(user.member)
        company.member_set.add(o_member)

        url = reverse("members:member-detail", args=[o_member.user.username])
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK

    def test_get_should_raise_not_found(self, api_client, user):
        """Ensure that when an invalid username, nothing is retrieved"""
        url = reverse("members:member-detail", args=[user.email])
        response = api_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_other_should_raise_not_found(self, api_client, user):
        """Ensure that a user can't retrieve other members"""
        debug_member = baker.make_recipe("members.tests.member")
        debug_user = debug_member.user
        url = reverse("members:member-detail", args=[debug_user.username])
        response = api_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_staff_get_other(self, api_client, user):
        """Ensure that a staff can retrieve other members"""
        user.is_staff = True
        user.is_superuser = True
        user.save(update_fields=["is_staff", "is_superuser"])

        debug_member = baker.make_recipe("members.tests.member")
        debug_user = debug_member.user
        url = reverse("members:member-detail", args=[debug_user.username])
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK

    def test_list(self, api_client, user):
        """Ensure that user can retrieve onlyself"""
        url = reverse("members:member-list")
        response = api_client.get(url)

        assert response.data["count"] == 1
        assert response.status_code == status.HTTP_200_OK

    def test_list_same_company(self, api_client, user, company, o_member):
        """Ensure that when in same company, all members are retrieved"""
        company.member_set.add(user.member)
        company.member_set.add(o_member)

        url = reverse("members:member-list")
        response = api_client.get(url)

        assert response.data["count"] == 2
        assert response.status_code == status.HTTP_200_OK

    def test_staff_list(self, api_client, user, o_member):
        """Ensure that a staff can retrieve all members"""
        user.is_staff = True
        user.is_superuser = True
        user.save(update_fields=["is_staff", "is_superuser"])

        baker.make_recipe("members.tests.member")
        url = reverse("members:member-list")
        response = api_client.get(url)

        assert response.data["count"] == Member.objects.count()
        assert response.status_code == status.HTTP_200_OK

    def test_update(self, api_client, user):
        """Ensure that when in same company, member is updated"""
        member = user.member
        member.function = MANAGER
        member.save(update_fields=["function"])

        payload = {"name": FAKE.name()}
        url = reverse("members:member-detail", args=[user.username])
        response = api_client.patch(url, payload)

        assert response.status_code == status.HTTP_200_OK

    def test_update_other(self, api_client, user, company, o_member):
        """Ensure that manager can update others"""
        member = user.member
        member.function = MANAGER
        member.save(update_fields=["function"])

        company.member_set.add(user.member)
        company.member_set.add(o_member)

        payload = {"name": FAKE.name()}
        url = reverse("members:member-detail", args=[o_member.user.username])
        response = api_client.patch(url, payload)

        assert response.status_code == status.HTTP_200_OK

    def test_update_should_raise_forbidden(self, api_client, user):
        """Ensure that only managers can update members"""
        payload = {"name": FAKE.name()}
        url = reverse("members:member-detail", args=[user.username])
        response = api_client.patch(url, payload)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_other_should_raise_not_found(self, api_client, user):
        """Ensure that when not in same company, nothing is updated"""
        member = user.member
        member.function = MANAGER
        member.save(update_fields=["function"])

        debug_member = baker.make_recipe("members.tests.member")
        debug_user = debug_member.user

        payload = {"name": FAKE.name()}
        url = reverse("members:member-detail", args=[debug_user.username])
        response = api_client.patch(url, payload)

        assert response.status_code == status.HTTP_404_NOT_FOUND
