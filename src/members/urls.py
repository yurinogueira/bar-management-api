# coding: utf-8
from django.conf.urls import include
from django.urls import path

from rest_framework.routers import DefaultRouter

from members.views import MemberViewSet

router = DefaultRouter()
router.register("member", MemberViewSet, "member")

urlpatterns = [
    path("", include(router.urls)),
]
