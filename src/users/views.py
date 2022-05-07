from django.db.models import Prefetch

from rest_framework import status, views
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from companies.models import Company
from members.models import Member
from users.models import User
from users.serializers import ResetPasswordSerializer, UserSerializer


class ResetPasswordViewSet(views.APIView):
    queryset = User.objects.all()
    serializer_class = ResetPasswordSerializer
    authentication_classes: list[object] = []
    permission_classes: list[object] = []

    def get_serializer(self, *args, **kwargs):
        return self.serializer_class(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.data.get("password")

        user = serializer.instance
        user.set_password(password)
        user.save(update_fields=["password"])

        return Response(status=status.HTTP_200_OK)


class UserViewSet(ReadOnlyModelViewSet):
    queryset = User.objects.select_related("member")
    serializer_class = UserSerializer

    lookup_field = "username"
    lookup_value_regex = "[\\w.@+-]+"

    def get_queryset(self):
        user = self.request.user
        queryset = self.queryset
        is_super = user.is_superuser

        if is_super:
            return queryset

        user = queryset.prefetch_related(
            Prefetch(
                "member__companies",
                queryset=Company.objects.prefetch_related(
                    Prefetch(
                        "member_set",
                        queryset=Member.objects.select_related("user"),
                        to_attr="prefetched_members",
                    )
                ),
                to_attr="prefetched_companies",
            )
        ).get(pk=user.pk)

        pks = [
            member.user.pk
            for company in user.member.prefetched_companies
            for member in company.prefetched_members
        ]

        return queryset.filter(pk__in=[*pks, user.pk])
