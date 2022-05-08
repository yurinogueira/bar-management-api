from faker import Faker
from model_bakery import baker
import pytest

from members.models import Member
from members.serializers import MemberSerializer

FAKE = Faker("pt_BR")


@pytest.mark.django_db
class TestMemberSerializer:
    def test_retrieve(self, member):
        """Ensure that member data is retrieved"""
        serializer = MemberSerializer(member)

        assert serializer.data["name"] == member.name

    def test_update(self, member):
        """Ensure that can update member data"""
        data = {"name": FAKE.name()}
        old_name = member.name

        serializer = MemberSerializer(member)
        serializer.update(member, data)

        assert member.name != old_name

    def test_retrieve_many(self):
        """Ensure that multiple members are retrieved"""
        baker.make_recipe("members.tests.member")
        baker.make_recipe("members.tests.member")
        baker.make_recipe("members.tests.member")
        serializer = MemberSerializer(Member.objects.all(), many=True)

        assert len(serializer.data) == Member.objects.count()
