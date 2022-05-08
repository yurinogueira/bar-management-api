from rest_framework import serializers

from members.models import Member


class MemberSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source="user.email")

    class Meta:
        model = Member
        fields = (
            "created_at",
            "updated_at",
            "name",
            "email",
            "function",
            "companies",
        )
