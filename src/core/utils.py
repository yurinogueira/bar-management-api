from django.db.models import Prefetch

from companies.models import Company


def related_queryset(queryset, user, p_queryset, r_prefetch, pk_get):
    if user.is_superuser:
        return queryset

    pk = pk_get(user.member)
    model = queryset.prefetch_related(
        Prefetch(
            r_prefetch,
            queryset=Company.objects.prefetch_related(
                Prefetch(
                    "member_set",
                    queryset=p_queryset,
                    to_attr="prefetched_members",
                )
            ),
            to_attr="prefetched_companies",
        )
    ).get(pk=pk)

    pks = [
        pk_get(member)
        for company in model.member.prefetched_companies
        for member in company.prefetched_members
    ]

    return queryset.filter(pk__in=[*pks, pk])
