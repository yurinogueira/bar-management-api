from rest_framework.mixins import UpdateModelMixin
from rest_framework.viewsets import ReadOnlyModelViewSet

from core.permissions import HasFunctionPermission
from core.utils import related_queryset
from members.models import Member
from members.serializers import MemberSerializer


class MemberViewSet(ReadOnlyModelViewSet, UpdateModelMixin):
    queryset = Member.objects.select_related("user")
    serializer_class = MemberSerializer
    permission_classes = [HasFunctionPermission]

    lookup_field = "user__username"
    lookup_value_regex = "[\\w.@+-]+"
    required_functions = {
        "retrieve": ["seller", "accountant", "manager"],
        "list": ["seller", "accountant", "manager"],
        "partial_update": ["manager"],
    }

    def get_queryset(self):
        return related_queryset(
            self.queryset,
            self.request.user,
            "companies",
            lambda x: x.pk,
            lambda x: x,
        )
