import pytest


@pytest.mark.django_db
class TestMemberModel:
    def test_member___str__(self, member):
        """Ensure that converting user to string return email"""
        member_name = member.name
        member_str = str(member)

        assert member_str == member_name
