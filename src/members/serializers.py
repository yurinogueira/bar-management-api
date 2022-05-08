from rest_framework import serializers

from members.models import Member


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        exclude = ("id",)
