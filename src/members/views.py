from rest_framework.mixins import UpdateModelMixin
from rest_framework.viewsets import ReadOnlyModelViewSet

from core.utils import related_queryset
from members.models import Member
from members.serializers import MemberSerializer


class MemberViewSet(ReadOnlyModelViewSet, UpdateModelMixin):
    queryset = Member.objects.select_related("user")
    serializer_class = MemberSerializer

    lookup_field = "user__username"
    lookup_value_regex = "[\\w.@+-]+"
    required_functions = {
        "retrieve": ["seller", "accountant", "manager"],
        "list": ["seller", "accountant", "manager"],
        "update": ["manager"],
    }

    def get_queryset(self):
        return related_queryset(
            self.queryset,
            self.request.user,
            Member.objects.all(),
            "companies",
            lambda x: x.pk,
        )
